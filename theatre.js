document.getElementById('playForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = {
      theme: document.getElementById('playTheme').value,
      setting: document.getElementById('playSetting').value,
      characters: document.getElementById('playCharacters').value,
  };

  try {
      const response = await fetch('/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      // Displaying the generated content
      document.getElementById('synopsis').textContent = data.synopsis;
      document.getElementById('promo').textContent = data.promo;

      // Enable download buttons
      document.getElementById('downloadSynopsisBtn').style.display = 'inline-block';
      document.getElementById('downloadPromoBtn').style.display = 'inline-block';

      // Add event listeners for download buttons
      document.getElementById('downloadSynopsisBtn').addEventListener('click', () => {
          downloadFile(data.synopsis, 'synopsis.txt');
      });

      document.getElementById('downloadPromoBtn').addEventListener('click', () => {
          downloadFile(data.promo, 'promo.txt');
      });
  } catch (error) {
      console.error("Error:", error);
  }
});

// Function to trigger file download
function downloadFile(content, filename) {
  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url); // Clean up after download
}
