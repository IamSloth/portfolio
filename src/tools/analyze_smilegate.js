import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../');

const TARGET_URL = 'https://careers.smilegate.com/apply/announce/view?seq=5759';

(async () => {
    console.log(`🚀 Launching Analyzer for Smilegate...`);
    console.log(`🔗 URL: ${TARGET_URL}`);

    const browser = await chromium.launch({ headless: true }); // Headless for analysis
    const page = await browser.newPage();
    
    try {
        await page.goto(TARGET_URL, { waitUntil: 'networkidle' });
        
        // 1. Get Job Title & Content
        const title = await page.title();
        const textContent = await page.evaluate(() => document.body.innerText);
        
        console.log(`✅ Page Loaded: ${title}`);

        // 2. Analyze Interactive Elements (Inputs, Buttons)
        // Need to check if there is an "Apply" button to click to see the form
        // Usually Smilegate has "지원하기" button.
        
        // Find '지원하기' button
        const applyButton = await page.getByText('지원하기', { exact: false }).first();
        let formInputs = [];
        
        if (await applyButton.isVisible()) {
             console.log("Found 'Apply' button. (Note: Actual form might need login)");
             // We won't click it in analysis mode to avoid login redirect issues in headless
        }

        const analysis = {
            company: 'Smilegate',
            url: TARGET_URL,
            title: title,
            textContent: textContent.substring(0, 10000)
        };
        
        // 3. Save Artifacts
        const companyDir = path.join(projectRoot, 'companies/smilegate');
        if (!fs.existsSync(companyDir)) fs.mkdirSync(companyDir, { recursive: true });
        
        fs.writeFileSync(path.join(companyDir, 'jd_analysis.json'), JSON.stringify(analysis, null, 2));
        fs.writeFileSync(path.join(companyDir, 'jd_full_text.txt'), textContent);
        
        console.log(`💾 Saved JD Analysis to: companies/smilegate/`);
        
    } catch (e) {
        console.error("❌ Analysis Failed:", e);
    } finally {
        await browser.close();
    }
})();