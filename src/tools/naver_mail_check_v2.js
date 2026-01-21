import { chromium } from 'playwright';
import fs from 'fs';

(async () => {
    console.log("🚀 Naver Mail Inspector V2 (Full Cycle)...");

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
    await page.waitForTimeout(3000); // Wait for load

    // Dump DOM
    console.log("📄 Dumping HTML...");
    const html = await page.content();
    fs.writeFileSync('naver_mail_full.html', html);
    console.log("✅ HTML Saved. Analyzing...");

    // Try to find list items using more generic selectors
    const mails = await page.evaluate(() => {
        // Try finding list items by common structure
        // Look for elements with 'subject' or 'title' in class
        const subjects = Array.from(document.querySelectorAll('[class*="subject"], [class*="title"]'))
            .filter(el => el.innerText.trim().length > 0)
            .slice(0, 10)
            .map(el => ({ 
                text: el.innerText.trim(), 
                class: el.className 
            }));
            
        const senders = Array.from(document.querySelectorAll('[class*="sender"], [class*="name"]'))
             .filter(el => el.innerText.trim().length > 0)
             .slice(0, 10)
             .map(el => ({
                 text: el.innerText.trim(),
                 class: el.className
             }));

        return { subjects, senders };
    });

    console.log("\n🔎 Potential Subjects Found:", mails.subjects);
    console.log("🔎 Potential Senders Found:", mails.senders);

    // Keep open
    await new Promise(() => {});

})();