chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scrape") {
    try {
      const heroSection = document.querySelector(".company-hero-info")
      if(heroSection){
        const link = heroSection.querySelector("a");
        if(link){
          sendResponse(link.href)
        }else{
          sendResponse("Domain not found!");
        }
      }else{
        sendResponse("HeroSection not found!");
      }

      sendResponse("Loop Break!");
    } catch (error) {
      // Send the error response if something goes wrong
      sendResponse({ success: false, error: error.message });
    }
  }
});
