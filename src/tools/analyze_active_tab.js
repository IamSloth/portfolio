import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../');

(async () => {
    console.log("🕵️ Connecting to Active Browser (Port 9222)...");
    
    try {
        const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
        const defaultContext = browser.contexts()[0];
        const pages = defaultContext.pages();
        
        // Find the active tab (assuming it's not 'about:blank' or Google if user navigated)
        // We'll take the last active one or filter.
        const page = pages.find(p => !p.url().includes('google.com') && !p.url().includes('about:blank')) || pages[0];
        
        await page.bringToFront();
        const url = page.url();
        const title = await page.title();
        
        console.log(`✅ Connected! Analyzing: [${title}]`);
        console.log(`🔗 URL: ${url}`);
        
        // 1. Extract Text Content (JD Analysis)
        const textContent = await page.evaluate(() => document.body.innerText);
        
        // 2. Extract Form Fields (Input Analysis)
        const inputs = await page.evaluate(() => {
            const els = Array.from(document.querySelectorAll('input, textarea, select, button'));
            return els.map(el => {
                // Try to find label
                let label = '';
                if (el.id) {
                    const labelEl = document.querySelector(`label[for="${el.id}"]`);
                    if (labelEl) label = labelEl.innerText;
                }
                if (!label && el.parentElement.tagName === 'LABEL') {
                    label = el.parentElement.innerText;
                }

                return {
                    tagName: el.tagName.toLowerCase(),
                    type: el.type,
                    name: el.name,
                    id: el.id,
                    placeholder: el.placeholder,
                    label: label.trim().replace(/\n/g, ' '),
                    isVisible: (el.offsetWidth > 0 && el.offsetHeight > 0)
                };
            });
        });

        // 3. Save Analysis
        const analysis = {
            timestamp: new Date().toISOString(),
            url: url,
            title: title,
            inputs: inputs,
            textContent: textContent.substring(0, 5000) // Limit size
        };
        
        const outputDir = path.join(projectRoot, 'output');
        if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);
        
        fs.writeFileSync(path.join(outputDir, 'target_page_analysis.json'), JSON.stringify(analysis, null, 2));
        fs.writeFileSync(path.join(outputDir, 'target_jd_text.txt'), textContent);
        
        console.log(`\n💾 Analysis Saved:`);
        console.log(`   - output/target_page_analysis.json (DOM Structure)`);
        console.log(`   - output/target_jd_text.txt (Job Description)`);
        
        console.log(`\n📊 Found ${inputs.length} interactive elements.`);
        
        // Attempt to identify Company Name from Title or URL
        let companyName = "unknown_company";
        if (url.includes("shiftup")) companyName = "shiftup";
        else if (url.includes("nexon")) companyName = "nexon";
        else if (url.includes("krafton")) companyName = "krafton";
        else {
             // Simple heuristic
             try {
                 const domain = new URL(url).hostname;
                 companyName = domain.split('.')[1] || domain;
             } catch(e) {}
        }
        
        console.log(`🏢 Detected Company: ${companyName}`);
        
        // Create Company Folder
        const companyDir = path.join(projectRoot, `companies/${companyName}`);
        if (!fs.existsSync(companyDir)) {
            fs.mkdirSync(companyDir, { recursive: true });
            console.log(`📂 Created Workspace: companies/${companyName}`);
        }

        browser.close();
        
    } catch (e) {
        console.error("❌ Failed to connect:", e);
        console.log("Make sure the browser was launched with 'launch_browser_debug.js'");
    }
})();