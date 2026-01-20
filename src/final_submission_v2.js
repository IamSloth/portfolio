import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function finalSubmissionV2() {
    console.log("🚀 Launching Clean Browser for THE FINAL Submission...");
    
    const browser = await chromium.launch({ 
        headless: false, 
        args: ['--start-maximized'] 
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    await page.goto('https://career.shiftup.co.kr/ko/o/78188/apply');

    // --- DATA ---
    const answers = [
        "홈페이지 (채용 사이트)",
        "1992-01-04",
        "경기도 광명시 도덕로 79, 1405호", // Updated Address
        "https://sites.google.com/view/jongkwon/"
    ];
    const info = { name: "임종권", email: "ssujklim@gmail.com", phone: "01040520834" };
    
    // NEW DESIGN RESUME PATH (V2)
    const resumePath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume_Design_v2.pdf');

    // --- EXECUTION ---
    console.log("Filling Form...");

    // 1. Text Fields
    await page.locator('input[id="이름"]').fill(info.name);
    await page.locator('input[id="이메일"]').fill(info.email);
    await page.locator('input[name*="전화번호"]').fill(info.phone);

    // 2. Textareas
    const textareas = await page.locator('textarea').all();
    for (let i = 0; i < textareas.length; i++) {
        if (i < answers.length) await textareas[i].fill(answers[i]);
    }

    // 3. Upload DESIGN Resume V2
    console.log(`Uploading Design Resume: ${path.basename(resumePath)}`);
    try {
        const fileInput = page.locator('input[type="file"]').first();
        await fileInput.setInputFiles(resumePath);
    } catch(e) { console.log("Upload Error:", e); }

    // 4. Checkboxes
    const checkboxes = await page.locator('input[type="checkbox"]').all();
    for (const box of checkboxes) {
        if (!(await box.isChecked())) await box.click({ force: true });
    }

    console.log("\n✅ READY TO SUBMIT. This is it!");
}

finalSubmissionV2();
