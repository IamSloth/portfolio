import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Naver Login Challenge (Self-Verifying)...");

    const browser = await chromium.launch({ 
        headless: false,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // 1. Login Logic
    await page.goto('https://nid.naver.com/nidlogin.login');
    
    const ID = 'deathbed0104';
    const PW = '##Rnjs002';

    await page.evaluate((id) => {
        const el = document.getElementById('id');
        el.value = id;
        el.dispatchEvent(new Event('input', { bubbles: true }));
    }, ID);

    await page.evaluate((pw) => {
        const el = document.getElementById('pw');
        el.value = pw;
        el.dispatchEvent(new Event('input', { bubbles: true }));
    }, PW);

    await page.waitForTimeout(500);
    await page.click('#log\\.login');

    // 2. Self-Verification (Am I logged in?)
    console.log("🕵️ Verifying Login Status...");
    
    try {
        // Wait for navigation to main page or generic naver domain
        // Or wait for specific element that appears only when logged in
        // e.g. '로그아웃' button or user info area
        
        // Strategy: Wait up to 5s for URL change or element
        await page.waitForFunction(() => {
            return location.href.includes('www.naver.com') || document.querySelector('.MyView-module__my_view___lqHk3'); // New Naver Main specific class
        }, { timeout: 5000 });

        console.log("✅ Login Success Verified! (Redirected to Main)");
        
        // Optional: Get User Name
        // ...

    } catch (e) {
        // Check for Captcha
        if (await page.locator('#captcha').count() > 0) {
            console.log("⚠️ Failed: Captcha Detected.");
        } else {
            console.log("⚠️ Login Verification Timeout. (Check screen)");
        }
    }

    // Keep browser open
    await new Promise(() => {}); 

})();