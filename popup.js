const fileInput = document.getElementById('fileInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const statusEl = document.getElementById('status');
const labelEl = document.getElementById('label');
const probEl = document.getElementById('prob');

analyzeBtn.addEventListener('click', async () => {
  labelEl.textContent = '';
  probEl.textContent = '';

  const file = fileInput.files && fileInput.files[0];
  if (!file) {
    statusEl.textContent = 'Please choose an image first.';
    return;
  }

  statusEl.textContent = 'Uploading and analyzing...';

  try {
    const formData = new FormData();
    formData.append('file', file, file.name || 'image');

    const resp = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: formData,
    });

    if (!resp.ok) {
      const t = await resp.text();
      throw new Error(t || `HTTP ${resp.status}`);
    }
    const data = await resp.json();
    const verdict = (data.label || '').toUpperCase();
    const prob = Number(data.prob_fake || 0).toFixed(3);

    labelEl.textContent = `Verdict: ${verdict}`;
    probEl.textContent = `Probability (fake): ${prob}`;
    statusEl.textContent = 'Done.';
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  }
});