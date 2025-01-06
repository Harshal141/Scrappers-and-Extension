chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scrape") {
    try {
      const title = document.querySelector(".company-profile-header-title").textContent;
      const domain = document.querySelector(".company-website-url").href;
      const industry = document.querySelector('span[name="industry_links"]');

      sendResponse({ success: true, data: { title, domain, industry } });
    } catch (error) {
      sendResponse({ success: false, error: error.message });
    }
  }
});
