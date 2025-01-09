chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "navigate_and_scrape") {
        (async () => {
            const { productList, startIndex, endIndex } = message;
            const selectedProducts = productList.filter(
                (product) => product.index >= startIndex && product.index <= endIndex
            );

            let allResults = [];
            const maxConcurrentTabs = 10;

            // Function to process each product with fallback mechanisms
            async function processProduct(product) {
                let httpsTab = null; // Tab for HTTPS
                let httpTab = null; // Tab for HTTP

                try {
                    // Try opening with HTTPS
                    console.log(`Trying HTTPS for product ID: ${product.index}`);
                    const httpsUrl = `https://${product.url}`;
                    httpsTab = await openAndScrapeTab({ ...product, url: httpsUrl });
                    return {
                        productID: product.index,
                        manufacturer_id: product.manufacturer_id,
                        url: httpsUrl,
                        extractedData: httpsTab.result,
                    };
                } catch (httpsError) {

                    console.error(`HTTPS failed for product ID: ${product.index}.`, httpsError);

                    if (httpsError?.id) {
                        await closeTab(httpsError.id); // Ensure HTTPS tab is closed
                    }

                    try {
                        // Fallback to HTTP
                        console.log(`Fallback to HTTP for product ID: ${product.index}`);
                        const httpUrl = `http://${product.url}`;
                        httpTab = await openAndScrapeTab({ ...product, url: httpUrl });
                        return {
                            productID: product.index,
                            manufacturer_id: product.manufacturer_id,
                            url: httpUrl,
                            extractedData: httpTab.result,
                        };
                    } catch (httpError) {
                        console.error(`HTTP failed for product ID: ${product.index}`, httpError);
                        if (httpError?.id) {
                            console.log("er g oit here");
                            await closeTab(httpError.id); // Ensure HTTPS tab is closed
                        }
                        return {
                            productID: product.index,
                            manufacturer_id: product.manufacturer_id,
                            url: product.url,
                            error: `Both HTTPS and HTTP failed: ${httpError.error.message}`,
                        };
                    }
                } finally {
                    // Ensure both tabs are closed
                    if (httpsTab?.id) {
                        console.log(`Closing HTTPS tab for ${product.url}`);
                        await closeTab(httpsTab.id);
                    }
                    if (httpTab?.id) {
                        console.log(`Closing HTTP tab for ${product.url}`);
                        await closeTab(httpTab.id);
                    }
                }
            }

            // Process products in batches for better efficiency
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
                            reject({
                                id: tab.id,
                                error: new Error(`Scraping failed for tab ID ${tab.id}: ${chrome.runtime.lastError?.message || 'No response received.'}`)
                            });                        } else {
                            resolve({ id: tab.id, result: response });
                        }
                    });
                }
            });

            setTimeout(() => {
                if (!tab) {
                    reject({
                        id: tab.id,
                        error: new Error(`Scraping failed for tab ID ${tab.id}: ${chrome.runtime.lastError?.message || 'No response received.'}`)
                    });
                }
            }, 8000);
        });
    });
}

// Helper function to close a tab with error handling
function closeTab(tabId) {
    return new Promise((resolve) => {
        if (tabId) {
            chrome.tabs.remove(tabId, () => {
                if (chrome.runtime.lastError) {
                    console.error(`Failed to close tab ID ${tabId}:`, chrome.runtime.lastError.message);
                } else {
                    console.log(`Tab ID ${tabId} closed successfully.`);
                }
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
