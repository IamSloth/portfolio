const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function analyzeTabs() {
    let browser;
    try {
        // Connect to the existing browser
        browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });

        const pages = await browser.pages();
        console.log(`Connected! Found ${pages.length} tabs.`);

        let jdContent = "";
        let formUrl = "";

        for (const page of pages) {
            const url = page.url();
            const title = await page.title();
            
            // Skip blank or system pages
            if (url === 'about:blank' || url.startsWith('chrome-extension')) continue;

            console.log(`\nAnalyzing Tab: [${title}] (${url})`);
            
            // Basic heuristic: Is this a form?
            const inputs = await page.$$('input, textarea, select');
            
            if (inputs.length > 5) {
                console.log("-> Identified as potential APPLICATION FORM");
                formUrl = url;
            } else {
                console.log("-> Identified as potential JOB DESCRIPTION (JD)");
                // Extract text content for analysis
                const content = await page.evaluate(() => document.body.innerText);
                jdContent += `\n\n--- TAB: ${title} ---\nURL: ${url}\n\n${content.substring(0, 5000)}... (truncated)\n`; // Limit size
            }
        }

        // Save JD analysis
        if (jdContent) {
            fs.writeFileSync(path.join(__dirname, '../output/Current_JD_Analysis.txt'), jdContent);
            console.log("\nSaved JD content to output/Current_JD_Analysis.txt");
        }

        return { jdContent, formUrl };

    } catch (error) {
        console.error("Error connecting to browser:", error);
    } finally {
        if (browser) browser.disconnect(); // Don't close the browser, just disconnect
    }
}

analyzeTabs();
