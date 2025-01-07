chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scrape") {
    try {
      // Extract the domain
      const domain = document.querySelector(".company-website-url").href;

      // Extract the industry text, including nested spans
      const industryElement = document.querySelector('span[name="industry_links"]');
      const industry = industryElement ? industryElement.innerText : null;

      // Extract the company description
      const descriptionElement = document.querySelector('[data-tracking-name="Company Description:"]');
      const description = descriptionElement ? descriptionElement.innerText : null;

      // Send the response with extracted data
      sendResponse({ domain, industry, description });
    } catch (error) {
      // Send the error response if something goes wrong
      sendResponse({ success: false, error: error.message });
    }
  }
});
