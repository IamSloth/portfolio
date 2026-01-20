import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function uploadKoreanResume() {
    console.log("Re-connecting for Resume Update...");
    
    // Launch new for stability in this demo
    const browser = await chromium.launch({ headless: false, args: ['--start-maximized'] });
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // Re-fill everything quickly to get to the upload state
    await page.goto('https://career.shiftup.co.kr/ko/o/78188/apply');
    
    // --- Data ---
    const answers = [
        "홈페이지 (채용 사이트)",
        "1992-01-04",
        "경기도 광명시",
        "https://sites.google.com/view/jongkwon/"
    ];
    const info = { name: "임종권", email: "ssujklim@gmail.com", phone: "01040520834" };
    
    // NEW KOREAN RESUME PATH
    const resumePath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume_KR.pdf');

    // --- Action ---
    // 1. Fill Text
    await page.locator('input[id="이름"]').fill(info.name);
    await page.locator('input[id="이메일"]').fill(info.email);
    await page.locator('input[name*="전화번호"]').fill(info.phone);

    const textareas = await page.locator('textarea').all();
    for (let i = 0; i < textareas.length; i++) {
        if (i < answers.length) await textareas[i].fill(answers[i]);
    }

    // 2. Upload NEW File
    console.log(`Uploading: ${path.basename(resumePath)}`);
    const fileInput = page.locator('input[type="file"]').first();
    await fileInput.setInputFiles(resumePath);

    // 3. Checkboxes
    const checkboxes = await page.locator('input[type="checkbox"]').all();
    for (const box of checkboxes) {
        if (!(await box.isChecked())) await box.click({ force: true });
    }

    console.log("\n✅ KOREAN RESUME UPLOADED. Ready to Submit.");
}

uploadKoreanResume();
