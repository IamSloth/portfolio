import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function correctApply() {
    console.log("Connecting to EXISTING demo browser (if possible) or launching new...");
    
    // For stability in this session, let's launch a NEW CLEAN window 
    // because connecting to the previous one without port info is tricky in this env.
    const browser = await chromium.launch({ 
        headless: false, 
        args: ['--start-maximized'] 
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    await page.goto('https://career.shiftup.co.kr/ko/o/78188/apply');

    // --- DATA ---
    const realAnswers = [
        "홈페이지 (채용 사이트)", // Q1: 지원 경로
        "1992-01-04",           // Q2: 생년월일
        "경기도 광명시",         // Q3: 주소
        "https://sites.google.com/view/jongkwon/" // Q4: 포트폴리오 URL (이력서에서 추출했던 값)
    ];

    const info = {
        name: "임종권",
        email: "ssujklim@gmail.com",
        phone: "01040520834"
    };

    const resumePath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume.pdf');

    // --- EXECUTION ---
    console.log("Filling Correct Data...");

    // 1. Basic Info
    await page.locator('input[id="이름"]').fill(info.name);
    await page.locator('input[id="이메일"]').fill(info.email);
    await page.locator('input[name*="전화번호"]').fill(info.phone);

    // 2. Textareas (Correct Mapping)
    const textareas = await page.locator('textarea').all();
    for (let i = 0; i < textareas.length; i++) {
        if (i < realAnswers.length) {
            await textareas[i].fill(realAnswers[i]);
            console.log(`Filled textarea ${i} with: ${realAnswers[i]}`);
        }
    }

    // 3. File Upload (Crucial!)
    console.log("Uploading Resume PDF...");
    try {
        const fileInput = page.locator('input[type="file"]').first();
        await fileInput.setInputFiles(resumePath);
    } catch(e) { console.log("Upload failed:", e); }

    // 4. Checkboxes
    console.log("Clicking Checkboxes...");
    const checkboxes = await page.locator('input[type="checkbox"]').all();
    for (const box of checkboxes) {
        try {
            if (!(await box.isChecked())) await box.click({ force: true });
        } catch(e) {}
    }

    console.log("\n✅ CORRECTION COMPLETE. Please review.");
}

correctApply();
