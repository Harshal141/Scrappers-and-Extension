chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "scrape") {
      try {
        const divs = document.querySelectorAll("div.item.image");
        const imageSources = Array.from(divs).map(div => div.querySelector("img").src);
        sendResponse({ success: true, images: imageSources });
      } catch (error) {
        sendResponse({ success: false, error: error.message });
      }
    }
  });
  