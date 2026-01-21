import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../');

const TARGET_URL = 'https://careers.smilegate.com/apply/announce/view?seq=5759';
const RESUME_PATH = path.resolve(projectRoot, 'output/Lim_JongKwon_Smilegate_CSR_Resume.pdf');

(async () => {
    console.log("🚀 Launching Assistant for Smilegate Application...");
    
    // Launch browser (Not headless, so user can interact)
    const browser = await chromium.launch({ 
        headless: false, 
        args: ['--start-maximized'] 
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // 1. Navigate to Job Page
    console.log(`🔗 Going to: ${TARGET_URL}`);
    await page.goto(TARGET_URL);
    
    // 2. Wait for User to Login & Reach Form
    console.log("\n🛑 [WAITING FOR USER]");
    console.log("1. Please click '지원하기' and LOGIN.");
    console.log("2. Navigate until you see the '지원서 작성' form.");
    console.log("3. Once the form is visible, come back here and press [ENTER] in the terminal (or I will retry in 60s).");
    
    // In this non-interactive terminal environment, we simulate a "Wait" by checking for a selector repeatedly.
    // We'll look for common form elements that appear after login.
    
    console.log("👀 Watching for Resume Upload field...");
    
    try {
        // Wait up to 5 minutes for user to login and reach the form
        // We look for file input or common resume fields
        await page.waitForSelector('input[type="file"], textarea[name*="intro"]', { timeout: 300000 });
        console.log("✅ Form Detected! Starting Auto-Fill...");
        
        // --- AUTO FILL LOGIC START ---
        
        // 1. Upload Resume (If file input exists)
        try {
            const fileInput = await page.locator('input[type="file"]').first();
            if (await fileInput.isVisible()) {
                console.log(`📂 Uploading Resume: ${path.basename(RESUME_PATH)}`);
                await fileInput.setInputFiles(RESUME_PATH);
            }
        } catch (e) { console.log("⚠️ Could not auto-upload file yet."); }

        // 2. Fill Basic Info (If fields exist)
        const info = {
            name: "임종권",
            email: "ssujklim@gmail.com",
            phone: "01040520834",
            address: "경기도 광명시 도덕로 79"
        };
        
        // Try various selectors for standard fields
        await page.getByLabel('이름', { exact: false }).fill(info.name).catch(() => {});
        await page.getByLabel('이메일', { exact: false }).fill(info.email).catch(() => {});
        await page.getByLabel('휴대전화', { exact: false }).fill(info.phone).catch(() => {});
        
        console.log("✨ Basic Info Filled (if found).");
        console.log("📝 Please review the form and submit manually.");
        
    } catch (e) {
        console.log("⏳ Time out waiting for form. Please run the script again once you are ready.");
    }
    
    // Keep browser open for user to finish
    await new Promise(() => {}); 
})();