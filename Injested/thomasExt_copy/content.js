chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scrape") {
    try {
      const links = [];

      const anchorTags = document.querySelectorAll('a[kind="dark"][rel="nofollow"]');

      anchorTags.forEach((a) => {
        const href = a.getAttribute("href");
        if (href) {
          links.push(href);
        }
      });

      sendResponse(links); // Send all collected hrefs, valid or not
    } catch (error) {
      sendResponse(["Error: " + error.message]);
    }

    return true; // Keep the message channel open for async response
  }
});
