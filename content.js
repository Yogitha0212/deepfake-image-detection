async function fetchImageAsDataUrl(url) {
  const resp = await fetch(url, { credentials: 'omit' });
  const blob = await resp.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

chrome.runtime.onMessage.addListener(async (msg, sender, sendResponse) => {
  if (msg && msg.type === 'CHECK_IMAGE' && msg.srcUrl) {
    try {
      const dataUrl = await fetchImageAsDataUrl(msg.srcUrl);
      const resp = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_base64: dataUrl }),
      });
      if (!resp.ok) {
        const t = await resp.text();
        throw new Error(t || `HTTP ${resp.status}`);
      }
      const data = await resp.json();
      const verdict = (data.label || '').toUpperCase();
      const prob = Number(data.prob_fake || 0).toFixed(3);
      alert(`Label: ${verdict}\nProbability (fake): ${prob}`);
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  }
});