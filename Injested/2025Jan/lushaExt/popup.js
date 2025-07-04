
document.getElementById("start").addEventListener("click", async () => {
    try {
      const productList = await fetch(chrome.runtime.getURL('source.json'))
        .then((response) => response.json());
  
      console.log("Product List:", productList);
  
      const response = await chrome.runtime.sendMessage({
        action: "navigate_and_scrape",
        productList: productList,
        startIndex: 213,
        endIndex: 4000, // end index included
        instances: 1, // no of tabs to run concurrently (make sure to have high internet speed and good processor)
        batchSize: 1000 // batches of extracted data which will be saved to the server at a time
      });
  
      console.log("Scraping Response:", response);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  });  
  