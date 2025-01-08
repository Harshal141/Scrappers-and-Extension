chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scrape") {
    try {
      const textData = document.querySelector("body").innerText;

      // Send the response with extracted data
      sendResponse({textData});
    } catch (error) {
      // Send the error response if something goes wrong
      sendResponse({ success: false, error: error.message });
    }
  }
});
