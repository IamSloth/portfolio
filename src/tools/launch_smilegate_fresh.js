import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Launching Fresh Browser (Debug Port 9222)...");
    
    // Launch new browser with remote debugging enabled
    const browser = await chromium.launch({ 
        headless: false, 
        args: [
            '--start-maximized',
            '--remote-debugging-port=9222' // Essential for connecting later
        ]
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // Navigate directly to Smilegate Job Post
    const TARGET_URL = 'https://careers.smilegate.com/apply/announce/view?seq=5759';
    console.log(`🔗 Navigating to: ${TARGET_URL}`);
    await page.goto(TARGET_URL);
    
    console.log("\n✅ Browser Ready!");
    console.log("👉 Step 1: Please LOGIN.");
    console.log("👉 Step 2: Click '지원하기' until you see the form.");
    console.log("👉 Step 3: Tell me 'Ready' or 'Fill now'.");

    // Keep process alive indefinitely
    await new Promise(() => {}); 
})();