import { chromium } from 'playwright';

(async () => {
    console.log("🚀 Naver Mail Inspector...");

    // Re-use session or Login again
    const browser = await chromium.launch({ 
        headless: false,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // Login First (Fast)
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
    await page.waitForNavigation(); // Wait for login

    // 1. Go to Mail
    console.log("📧 Navigating to Mail...");
    await page.goto('https://mail.naver.com/');

    // 2. Inspect Mail List
    console.log("👀 Reading Mail List...");
    // Wait for list to load
    await page.waitForSelector('.mail_list, .mail_list_wrap, #list_for_view');
    
    // Extract Subjects and Senders
    const mails = await page.evaluate(() => {
        // Selectors might vary (New Naver Mail vs Old)
        // Trying generic selectors
        const rows = Array.from(document.querySelectorAll('li.mail_item, tr.mail_list_item'));
        
        return rows.slice(0, 5).map(row => {
            const sender = row.querySelector('.mail_sender, .name')?.innerText.trim() || 'Unknown';
            const subject = row.querySelector('.mail_title, .subject')?.innerText.trim() || 'No Title';
            const time = row.querySelector('.mail_date, .time')?.innerText.trim() || '';
            return { sender, subject, time };
        });
    });

    console.log("\n📬 Recent 5 Emails:");
    mails.forEach((m, i) => {
        console.log(`[${i+1}] ${m.sender}: ${m.subject} (${m.time})`);
    });

    // Keep open
    await new Promise(() => {});

})();