import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Reading Hackathon Email (Force Mode)...");

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
    await page.waitForTimeout(3000);

    // Click Email
    console.log("🔍 Finding Hackathon Email...");
    // Try to find the specific email row first
    const emailLink = page.locator('.mail_title_link').filter({ hasText: '해커톤' }).first();
    
    if (await emailLink.isVisible()) {
        console.log("🖱️ Force Clicking Email...");
        await emailLink.click({ force: true }); // FORCE CLICK
        
        await page.waitForTimeout(3000); // Wait for content load
        
        // Extract Body
        console.log("📝 Extracting Content...");
        const content = await page.evaluate(() => {
            // Try various containers for mail body
            const containers = [
                '.mail_view_contents', 
                '.read_body', 
                '#readFrame', 
                '.mail_view_body',
                '.view_content'
            ];
            
            for (const selector of containers) {
                const el = document.querySelector(selector);
                if (el && el.innerText.trim().length > 0) {
                    return el.innerText.trim();
                }
            }
            
            // If main body not found, try iframe if present
            const iframe = document.querySelector('iframe#readFrame');
            if (iframe) {
                try {
                    return iframe.contentWindow.document.body.innerText;
                } catch(e) { return "Iframe detected but access denied (CORS)"; }
            }

            return "⚠️ Body content not found. Dumping visible text: " + document.body.innerText.substring(0, 500);
        });
        
        console.log("\n================ [ HACKATHON EMAIL CONTENT ] ================");
        console.log(content);
        console.log("=============================================================\n");
        
    } else {
        console.log("⚠️ Could not find email with '해커톤' in title.");
    }

    // Close after success
    await browser.close();

})();