import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Reading Hackathon Email...");

    const browser = await chromium.launch({ 
        headless: false,
        args: ['--start-maximized']
    });
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // Login
    await page.goto('https://nid.naver.com/nidlogin.login');
    const ID = 'deathbed0104';
    const PW = '##Rnjs002';

    await page.evaluate((id) => {
        document.getElementById('id').value = id;
        document.getElementById('id').dispatchEvent(new Event('input', { bubbles: true }));
    }, ID);
    await page.evaluate((pw) => {
        document.getElementById('pw').value = pw;
        document.getElementById('pw').dispatchEvent(new Event('input', { bubbles: true }));
    }, PW);
    await page.click('#log\\.login');
    await page.waitForNavigation();

    // Mail
    console.log("📧 Going to Mail...");
    await page.goto('https://mail.naver.com/');
    await page.waitForTimeout(2000);

    // Click Email
    console.log("🔍 Finding Hackathon Email...");
    const emailLink = page.locator('.mail_title_link').filter({ hasText: '해커톤' }).first();
    
    if (await emailLink.isVisible()) {
        await emailLink.click();
        console.log("🖱️ Clicked Email!");
        
        await page.waitForTimeout(2000); // Wait for body load
        
        // Extract Body
        // Selectors for mail body vary, usually inside an iframe or a specific div
        // Trying generic content selectors
        const content = await page.evaluate(() => {
            const body = document.querySelector('.mail_view_contents, .read_body, #readFrame');
            return body ? body.innerText : "⚠️ Body content not found with standard selectors.";
        });
        
        console.log("\n================ [ EMAIL CONTENT ] ================");
        console.log(content.substring(0, 1000)); // Print first 1000 chars
        console.log("===================================================\n");
        
    } else {
        console.log("⚠️ Could not find email with '해커톤' in title.");
    }

    // Keep open for verification
    await new Promise(() => {});

})();