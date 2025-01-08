chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "navigate_and_scrape") {
      (async () => {
        const { productList, startIndex, endIndex } = message;
  
        const selectedProducts = productList.filter(
          (product) => product.index >= startIndex && product.index <= endIndex
        );
        console.log("Selected Products:", selectedProducts);

        const scrapingResults = [];
        
        // Sequentially process each product
        for (const product of selectedProducts) {
          console.log(`Processing product ID: ${product.id} (Index: ${product.index})`);
  
          try {
            // Open a new tab and wait for the navigation to complete
            const tab = await openAndScrapeTab(product);
  
            // Capture the result and close the tab
            scrapingResults.push({
              "productID" : product.id,
              "heroImg" : product.imageurl,
              "sliderImg" : tab.result
            });

            await closeTab(tab.id);
  
          } catch (error) {
            console.error(`Error processing product ID: ${product.id}`, error);
          }
        }
  
        // Send the collected results back to the popup or content script
        console.log("Scraping results:", scrapingResults);
        sendResponse(scrapingResults);
      })();
  
      return true; // Indicates that the response is asynchronous
    }
  });
  
  // Helper function to open a new tab and scrape
  function openAndScrapeTab(product) {
    return new Promise((resolve, reject) => {
      chrome.tabs.create({ url: `https://www.richsusa.com/products///${product.id}/` }, (tab) => {
        chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
          if (tabId === tab.id && changeInfo.status === 'complete') {
            chrome.tabs.sendMessage(tabId, { action: 'scrape' }, (response) => {
              chrome.tabs.onUpdated.removeListener(listener);
              
              if (chrome.runtime.lastError || !response) {
                reject(new Error(`Scraping failed for tab ID ${tab.id}`));
              } else {
                resolve({ id: tab.id, result: response });
              }
            });
          }
        });
      });
    });
  }
  
  // Helper function to close a tab
  function closeTab(tabId) {
    return new Promise((resolve) => {
      chrome.tabs.remove(tabId, () => resolve());
    });
  }