import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Naver Login Challenge...");

    const browser = await chromium.launch({ 
        headless: false,
        args: ['--start-maximized'] // Maximize for better visibility
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // 1. Navigate to Naver Login
    await page.goto('https://nid.naver.com/nidlogin.login');
    console.log("🔗 Opened Naver Login Page");

    // 2. Input Credentials (ID)
    // Naver detects 'bot-like' typing.
    // Strategy: JavaScript Value Injection (Bypasses keystroke analysis)
    const ID = 'deathbed0104';
    const PW = '##Rnjs002';

    console.log("✍️ Entering ID...");
    await page.evaluate((id) => {
        const el = document.getElementById('id');
        el.value = id;
        el.dispatchEvent(new Event('input', { bubbles: true })); // Trigger listeners
    }, ID);

    // 3. Input Credentials (PW)
    console.log("✍️ Entering PW...");
    await page.evaluate((pw) => {
        const el = document.getElementById('pw');
        el.value = pw;
        el.dispatchEvent(new Event('input', { bubbles: true }));
    }, PW);

    // 4. Click Login Button
    console.log("🖱️ Clicking Login...");
    // Wait a bit to seem human
    await page.waitForTimeout(1000);
    
    const loginBtn = page.locator('#log\\.login');
    await loginBtn.click();

    // 5. Check Result
    // Wait to see if navigation happens or captcha appears
    try {
        await page.waitForNavigation({ timeout: 5000 });
        console.log("✅ Navigation happened (Likely Success)");
    } catch (e) {
        // If navigation didn't happen, check for captcha or error
        const captcha = await page.locator('#captcha').count();
        if (captcha > 0) {
            console.log("⚠️ Captcha detected! (Bot detected)");
        } else {
            console.log("ℹ️ No navigation, but no captcha detected immediately.");
        }
    }

    // Keep browser open for user to see
    console.log("👀 Browser remains open. Check the result.");
    await new Promise(() => {}); 

})();