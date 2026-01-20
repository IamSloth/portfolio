import { chromium } from 'playwright';

async function analyzePortfolio() {
    console.log("🔍 Deep Diving into Portfolio...");
    
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    // User's portfolio URL
    const url = 'https://sites.google.com/view/jongkwon/';
    
    try {
        await page.goto(url, { waitUntil: 'networkidle' });
        
        // Scrape visible text to understand projects
        const content = await page.evaluate(() => document.body.innerText);
        
        console.log("--- Portfolio Content Extracted ---");
        console.log(content.substring(0, 2000)); // Print first 2000 chars for AI analysis
        
    } catch (e) {
        console.error("Error scraping portfolio:", e);
    } finally {
        await browser.close();
    }
}

analyzePortfolio();
