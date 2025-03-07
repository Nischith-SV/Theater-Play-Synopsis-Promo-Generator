from flask import Flask, request, jsonify, render_template
import requests
import re
import logging

app = Flask(__name__)

# Third-party API URL (replace with your API endpoint)
THIRD_PARTY_API_URL = "https://chat.ivislabs.in/api/chat/completions"

# Hardcoded API key (replace with your actual API key)
API_KEY = "sk-0f9588a2f23345709b4006ce960db71f"

# Headers for the third-party API
API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def clean_text(text):
    """
    Cleans the text by removing markdown or unnecessary symbols.
    """
    text = re.sub(r'#.*\n', '', text)  # Removes lines starting with '#'
    text = re.sub(r'\*\*.*?\*\*', '', text)  # Removes bold formatting (e.g., **text**)
    text = re.sub(r'\*.*?\*', '', text)  # Removes italic formatting (e.g., *text*)
    text = re.sub(r'\n+', ' ', text)  # Removes extra newlines
    text = re.sub(r'^\s+|\s+?$', '', text)  # Strips leading and trailing whitespaces

    return text

def generate_content(prompt):
    """
    Sends a prompt to the third-party API and returns the generated content.
    """
    payload = {
        "model": "gemma2:2b",  # Replace with a valid model name
        "messages": [{"role": "user", "content": prompt}],  # Example structure
        "max_tokens": 300,  # Adjust as needed
        "temperature": 0.7  # Adjust as needed
    }

    logging.debug(f"Sending payload to API: {payload}")

    try:
        response = requests.post(THIRD_PARTY_API_URL, headers=API_HEADERS, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        return f"Other error occurred: {err}"

    logging.debug(f"API response status code: {response.status_code}")
    logging.debug(f"API response content: {response.text}")

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No content generated.")
    else:
        return f"Error: {response.status_code} - {response.text}"

def generate_synopsis(theme, setting, characters):
    """
    Generates a synopsis using the third-party API.
    """
    prompt = f"Generate a detailed synopsis for a play with the theme '{theme}', set in '{setting}', and featuring the characters '{characters}'."
    return generate_content(prompt)

def generate_promo(theme, setting, characters):
    """
    Generates a promotional description using the third-party API.
    """
    prompt = f"Write a promotional description for a play with the theme '{theme}', set in '{setting}', and featuring the characters '{characters}'."
    return generate_content(prompt)

@app.route('/')
def home():
    """
    Serves the frontend HTML page.
    """
    return render_template('theatre.html')

@app.route('/generate', methods=['POST'])
def generate():
    """
    Handles the generation request from the frontend.
    """
    try:
        data = request.json
        logging.debug(f"Received data: {data}")  # Debugging line

        if not data:
            return jsonify({"error": "No data received"}), 400

        theme = data.get('theme')
        setting = data.get('setting')
        characters = data.get('characters')

        if not theme or not setting or not characters:
            return jsonify({"error": "Missing required fields"}), 400

        logging.debug(f"Generating synopsis...")  # Debugging line
        synopsis = generate_synopsis(theme, setting, characters)
        logging.debug(f"Generated synopsis: {synopsis}")  # Debugging line

        logging.debug(f"Generating promo...")  # Debugging line
        promo = generate_promo(theme, setting, characters)
        logging.debug(f"Generated promo: {promo}")  # Debugging line

        return jsonify({
            'synopsis': synopsis,
            'promo': promo
        })
    except Exception as e:
        logging.error(f"Error in /generate route: {str(e)}")  # Debugging line
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
