import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Launching Browser for Manual Navigation...");
    
    // Launch browser in visible mode
    const browser = await chromium.launch({ 
        headless: false, 
        args: ['--start-maximized'] // Start maximized
    });
    
    // Create a new context with no viewport limit (responsive)
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // Navigate to Google as a starting point
    await page.goto('https://www.google.com');
    
    console.log("\n🌐 Browser is ready!");
    console.log("👉 Please navigate to the job application page.");
    console.log("👉 I will wait here until you are ready (Press Ctrl+C to stop script, but browser will stay open if detached).");

    // Keep the script running to prevent the browser from closing immediately
    // In a real scenario, we might want to attach a listener or just wait indefinitely
    await new Promise(() => {}); 
})();