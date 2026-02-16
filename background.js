chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'checkImage',
    title: 'Check image for deepfake',
    contexts: ['image']
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'checkImage' && info.srcUrl && tab && tab.id) {
    // Ensure the content script is present in the target tab/frame before sending a message (MV3 service workers can be cold-started)
    try {
      await chrome.scripting.executeScript({
        target: { tabId: tab.id, frameIds: info.frameId ? [info.frameId] : undefined },
        files: ['content.js']
      });
    } catch (e) {
      // Likely already injected; ignore
      console.debug('executeScript warning:', e && e.message ? e.message : e);
    }

    const message = { type: 'CHECK_IMAGE', srcUrl: info.srcUrl };
    // Use callback form to gracefully handle "Receiving end does not exist" without throwing an unhandled promise error
    try {
      chrome.tabs.sendMessage(tab.id, message, { frameId: info.frameId }, function () {
        if (chrome.runtime.lastError) {
          console.warn('Could not establish connection:', chrome.runtime.lastError.message);
        }
      });
    } catch (err) {
      console.warn('tabs.sendMessage error:', err && err.message ? err.message : err);
    }
  } else {
    console.warn('Context click missing tab/srcUrl or wrong menu item.');
  }
});