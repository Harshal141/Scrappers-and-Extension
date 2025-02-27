// Load URLs from the JSON file
fetch(chrome.runtime.getURL('companies.json'))
    .then(response => response.json())
    .then(data => {
        const urls = data.map(item => item.website); // Assuming "website" is the key in companies.json
        console.log("Loaded URLs:", urls);

        // Open each URL in a new tab
        urls.forEach((url, index) => {
            setTimeout(() => {
                chrome.tabs.create({ url: url, active: false });
            }, index * 1000); // Opens a new tab every second to avoid performance issues
        });
    })
    .catch(error => console.error("Error loading URLs:", error));
