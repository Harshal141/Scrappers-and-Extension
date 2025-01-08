chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "navigate_and_scrape") {
        (async () => {
            const { productList, startIndex, endIndex } = message;
            const selectedProducts = productList.filter(
                (product) => product.index >= startIndex && product.index <= endIndex
            );

            let allResults = [];
            const maxConcurrentTabs = 10;

            const processProduct = async (product) => {
                console.log(`Processing product ID: ${product.index}`);
                let tab = null; // Declare tab outside the try block
                try {
                    tab = await openAndScrapeTab(product); // Assign tab here
                    return {
                        productID: product.index,
                        url: product.url,
                        extractedData: tab.result,
                    };
                } catch (error) {
                    console.error(`Error processing product ID: ${product.index}`, error);
                    return null; // Handle errors gracefully
                } finally {
                    // Close tab only if it was successfully opened
                    if (tab?.id) {
                        await closeTab(tab.id);
                    }
                }
            };

            const processInBatches = async (products) => {
                for (let i = 0; i < products.length; i += maxConcurrentTabs) {
                    const batch = products.slice(i, i + maxConcurrentTabs);
                    const batchResult = await Promise.all(batch.map(processProduct));
                    allResults.push(...batchResult);

                    if (allResults.length >= 1000) {
                        console.log("Scraping results batch:", allResults);
                        
                        // Send results to the server
                        await sendDataToServer(allResults);
                        
                        allResults = []; // Reset results after logging
                    }
                }
            };

            await processInBatches(selectedProducts);

            // Final log for remaining results
            if (allResults.length > 0) {
                console.log("Final scraping results:", allResults);
                
                // Send final results to the server
                await sendDataToServer(allResults);
            }

            sendResponse(allResults);
        })();

        return true;
    }
});

// Helper function to open a new tab and scrape
function openAndScrapeTab(product) {
    return new Promise((resolve, reject) => {
        chrome.tabs.create({ url: product.url }, (tab) => {
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
        if (tabId) {
            chrome.tabs.remove(tabId, () => resolve());
        } else {
            resolve();
        }
    });
}

// Helper function to send data to the Node.js server
async function sendDataToServer(data) {
    try {
        const response = await fetch('http://localhost:3000/store', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        console.log("Server response:", result);
    } catch (error) {
        console.error("Error sending data to server:", error);
    }
}
