chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scrape") {
    try {
      // Locate the website section and extract the first link
      const websiteSection = document.querySelector(".business-details-section-column_column__ltcSo");
      if (websiteSection) {
        const link = websiteSection.querySelector('a[href*="http"]'); // Find the first valid link
        if (link) {
          sendResponse(link.href);
        } else {
          sendResponse("Domain not found!");
        }
      } else {
        sendResponse("Domain not found!");
      }
    } catch (error) {
      // Catch any errors and respond
      sendResponse("Error: " + error.message);
    }
    return true;
  }
});


// function scrapeData() {
//   try {
//       const showcase = document.querySelector(".search-results_supplierListContainer__tD4DJ");
//       if (!showcase) return { error: "Company list not found!" };

//       const companies = showcase.querySelectorAll(".search-result-supplier_searchResultSupplierPanel__HdR9H");
//       let pageData = [];

//       companies.forEach(coman => {
//           try {
//               let supplierLink = coman.querySelector("h2.mar-r-1.txt-medium a");
//               if (supplierLink) {
//                   pageData.push({
//                       name: supplierLink.innerText.trim(),
//                       relDomain: supplierLink.href
//                   });
//               }
//           } catch (error) {
//               console.error("Error extracting company:", error);
//           }
//       });

//       return pageData.length ? pageData : { error: "No companies found!" };
//   } catch (error) {
//       return { error: "Scraping error: " + error.message };
//   }
// }

// // Ensure response is always sent
// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//   if (message.action === "scrape") {
//       let data = scrapeData();
//       sendResponse(data);
//   }
//   return true; // Keep the message port open for async responses
// });
