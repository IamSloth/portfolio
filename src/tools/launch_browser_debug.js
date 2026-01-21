import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Launching Browser in DEBUG MODE (Port 9222)...");
    
    // Launch with Remote Debugging enabled
    const browser = await chromium.launch({ 
        headless: false, 
        args: [
            '--start-maximized',
            '--remote-debugging-port=9222' // <--- This allows us to connect later!
        ]
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    await page.goto('https://www.google.com');
    
    console.log("\n👀 'Magic Eye' Enabled!");
    console.log("👉 Please navigate to the Job Page again.");
    console.log("👉 Once you are there, tell me 'Analyze now'!");

    // Keep alive
    await new Promise(() => {}); 
})();