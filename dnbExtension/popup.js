
document.getElementById("start").addEventListener("click", async () => {
    try {
      const productList = await fetch(chrome.runtime.getURL('source.json'))
        .then((response) => response.json());
  
      console.log("Product List:", productList);
  
      const response = await chrome.runtime.sendMessage({
        action: "navigate_and_scrape",
        productList: productList,
        startIndex: 5000,
        endIndex: 10000,
      });
  
      console.log("Scraping Response:", response);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  });  
  