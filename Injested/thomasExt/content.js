chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scrape") {
    try {
      // Locate the website section and extract the first link
      const websiteSection = document.querySelector(".business-details-section-column_column__ltcSo");
      if (websiteSection) {
        const link = websiteSection.querySelector('a[href*="http"]'); // Find the first valid link
        if (link) {
          sendResponse(link.href);
        } else {
          sendResponse("Domain not found!");
        }
      } else {
        sendResponse("Website section not found!");
      }
    } catch (error) {
      // Catch any errors and respond
      sendResponse("Error: " + error.message);
    }
    return true;
  }
});
