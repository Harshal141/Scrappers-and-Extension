
document.getElementById("start").addEventListener("click", async () => {
    try {
      // Fetch the JSON data
      const productList = await fetch(chrome.runtime.getURL('source.json'))
        .then((response) => response.json());
  
      console.log("Product List:", productList);
  
      // Send message to the background script
      const response = await chrome.runtime.sendMessage({
        action: "navigate_and_scrape",
        productList: productList, // Include the fetched data
        startIndex: 1,
        endIndex: 1113,
      });
  
      console.log("Scraping Response:", response);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  });  
  