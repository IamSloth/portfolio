import { chromium } from 'playwright';
import fs from 'fs';

(async () => {
    console.log("🔍 Inspecting Mail DOM...");

    const browser = await chromium.connectOverCDP('http://127.0.0.1:9222'); // Reconnect to existing
    const defaultContext = browser.contexts()[0];
    const pages = defaultContext.pages();
    const page = pages.find(p => p.url().includes('mail.naver.com')) || pages[0];

    // Dump HTML of the mail list area
    // Look for a large container likely holding the list
    const html = await page.evaluate(() => {
        const list = document.querySelector('#list_for_view') || document.querySelector('.mail_list_wrap') || document.body;
        return list.innerHTML.substring(0, 20000); // First 20k chars
    });

    fs.writeFileSync('mail_dom_dump.html', html);
    console.log("📄 DOM Dump saved to mail_dom_dump.html");
    
    // Quick peek at class names
    const classNames = await page.evaluate(() => {
        const classes = new Set();
        document.querySelectorAll('*').forEach(el => {
            el.classList.forEach(c => classes.add(c));
        });
        return Array.from(classes).filter(c => c.includes('subject') || c.includes('title') || c.includes('sender'));
    });
    
    console.log("🔎 Potential Classes Found:", classNames);

})();