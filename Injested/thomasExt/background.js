chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "navigate_and_scrape") {
        (async () => {
            const { productList, startIndex, endIndex, instances, batchSize } = message;
            const selectedProducts = productList.filter(
                (product) => product.index >= startIndex && product.index <= endIndex
            );

            let allResults = [];
            const maxConcurrentTabs = instances;

            // Function to process each product with fallback mechanisms
            async function processProduct(product) {
                let httpsTab = null; // Tab for HTTPS

                try {
                    console.log("Processing: ", product.url," " , product.index);
                    httpsTab = await openAndScrapeTab(product);
                    console.log("Scraping result:", httpsTab.result);
                    // return httpsTab.result;
                    return {
                        name: httpsTab.result.name,
                        domain: httpsTab.result.domain,
                    };
                } catch (httpsError) {

                    console.error(`HTTP failed for ${product.url}`, httpsError);
                    await closeTab(httpsError.id)
                    return {
                        name: product.name,
                        error: `Failed to scrape: ${httpsError.error.message}`,
                    };
                } finally {
                    if (httpsTab?.id) {
                        await closeTab(httpsTab.id);
                    }
                }
            }

            function delay(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }

            // Process products in batches for better efficiency
            const processInBatches = async (products) => {
                for (let i = 0; i < products.length; i += maxConcurrentTabs) {
                    const batch = products.slice(i, i + maxConcurrentTabs);
                    const batchResult = await Promise.all(batch.map(processProduct));
                    allResults.push(...batchResult);

                    if (allResults.length >= batchSize) {
                        console.log("Scraping results batch:", allResults);
                        
                        // Send results to the server
                        await sendDataToServer(allResults);
                        
                        allResults = []; // Reset results after logging
                    }
                    console.log("Waiting for 5 seconds before processing the next batch...");
                    await delay(5000);  // TODO: add randomaizer in this
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

function openAndScrapeTab(product) {
    return new Promise((resolve, reject) => {
        chrome.tabs.create({ url: product.url }, (tab) => {

            const timeout = setTimeout(() => {
                reject({
                    id: tab.id,
                    error: new Error(`Page took too long to load: ${product.url}`)
                });
            }, 20000); // 20 seconds timeout if not mark page as not resonding

            chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
                if (tabId === tab.id && changeInfo.status === 'complete') {
                    clearTimeout(timeout); // Clear the timeout once the page is loaded
                    chrome.tabs.sendMessage(tabId, { action: 'scrape' }, (response) => {
                        chrome.tabs.onUpdated.removeListener(listener);
                        if (chrome.runtime.lastError || !response) {
                            reject({
                                id: tab.id,
                                error: new Error(`Scraping failed for tab ID ${tab.id}: ${chrome.runtime.lastError?.message || 'No response received.'}`)
                            });
                        } else {
                            resolve({ id: tab.id, result: response });
                        }
                    });
                }
            });
        });
    });
}


// Helper function to close a tab with error handling
function closeTab(tabId) {
    return new Promise((resolve) => {
        if (tabId) {
            chrome.tabs.remove(tabId, () => {
                resolve();
            });
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
