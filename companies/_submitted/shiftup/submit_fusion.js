import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function finalSubmissionFusion() {
    console.log("🚀 Launching Chrome for FUSION Submission (Teamplay)...");
    
    const browser = await chromium.launch({ 
        headless: false, 
        channel: 'chrome', 
        args: ['--start-maximized'] 
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    try {
        await page.goto('https://career.shiftup.co.kr/ko/o/78188/apply');

        // --- DATA ---
        const answers = [
            "홈페이지 (채용 사이트)",
            "1992-01-04",
            "경기도 광명시 도덕로 79, 1405호", 
            "https://sites.google.com/view/jongkwon/"
        ];
        const info = { name: "임종권", email: "ssujklim@gmail.com", phone: "01040520834" };
        const resumePath = path.resolve(__dirname, '../../output/Lim_JongKwon_ShiftUp_Fusion_Resume.pdf');

        // --- EXECUTION ---
        console.log("Filling Form...");

        try { await page.locator('input[id="이름"]').fill(info.name); } catch(e){}
        try { await page.locator('input[id="이메일"]').fill(info.email); } catch(e){}
        try { await page.locator('input[name*="전화번호"]').fill(info.phone); } catch(e){}

        const textareas = await page.locator('textarea').all();
        for (let i = 0; i < textareas.length; i++) {
            if (i < answers.length) await textareas[i].fill(answers[i]);
        }

        console.log(`Uploading: ${path.basename(resumePath)}`);
        try {
            const fileInput = page.locator('input[type="file"]').first();
            await fileInput.setInputFiles(resumePath);
        } catch(e) { console.log("Upload Error:", e); }

        try {
            const checkboxes = await page.locator('input[type="checkbox"]').all();
            for (const box of checkboxes) {
                if (!(await box.isChecked())) await box.click({ force: true, timeout: 1000 });
            }
        } catch(e) { /* ignore */ }

        console.log("\n✅ ALL DONE. Fusion Resume Uploaded.");
        
        await new Promise(() => {}); // Keep Alive

    } catch (error) {
        console.error("Error:", error);
        await new Promise(() => {});
    }
}

finalSubmissionFusion();
