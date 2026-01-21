import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function executePerfectApply() {
    let browser;
    try {
        console.log("Connecting to Chrome...");
        browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
        const context = browser.contexts()[0];
        const pages = context.pages();
        const page = pages.find(p => p.url().includes('career.shiftup.co.kr')) || pages[0];
        
        console.log(`Target Page: ${await page.title()}`);
        await page.bringToFront();

        // --- DATA ---
        const info = {
            name: "임종권",
            email: "ssujklim@gmail.com",
            phone: "01040520834"
        };
        const resumePath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume.pdf');
        
        const answers = {
             q1: `[게임 개발 환경의 안정성을 책임지는 'Tech-Savvy' 총무 전문가]
시프트업이 글로벌 게임 시장에서 혁신을 만들어가는 동안, 저는 그 혁신의 기반이 되는 임직원들의 업무 환경을 가장 안정적으로 지켜내고 싶습니다. 저는 단순한 자산 관리자가 아닙니다. 전기공학 전공 지식을 바탕으로 IT 자산의 하드웨어적 이슈를 직접 진단하고, 6년간의 총무 경력으로 자산 수명 주기(Life-cycle)를 체계적으로 관리해 온 '기술 기반 운영 전문가'입니다. 시프트업의 소중한 유무형 자산을 빈틈없이 관리하여 개발자분들이 오직 창작에만 몰입할 수 있는 최적의 환경을 제공하겠습니다.

첫째, 개발자와 말이 통하는 하드웨어 트러블슈터입니다.
전기공학 학사 및 IoT 하드웨어 제조 경력을 보유하고 있어, PC/서버/네트워크 장비의 물리적 구조를 깊이 이해하고 있습니다. 단순 고장 접수 처리에 그치지 않고, 1차적으로 원인을 규명하고 해결하여 불필요한 외주 비용과 대기 시간을 획기적으로 줄일 수 있습니다.`,
             
             q2: `둘째, 갈등을 해결하는 유연한 커뮤니케이션 능력입니다.
사회복지사 1급 자격을 통해 훈련된 공감 및 갈등 조정 능력으로 다양한 직군이 모인 게임사 조직 내에서 발생할 수 있는 요청 사항들을 원만하게 조율하겠습니다. 규정은 준수하되, 구성원의 입장을 배려하는 '해결 지향적' 지원을 약속드립니다.

입사 즉시 보유하고 있는 자산 관리 노하우와 1종 대형 면허의 기동력을 활용하여 사옥 관리 및 임직원 지원 업무에 공백이 없도록 하겠습니다. 장기적으로는 시프트업의 자산 관리 프로세스를 데이터화하여 예산 낭비를 막고 효율을 극대화하는 스마트한 총무 시스템을 구축하겠습니다.`
        };

        // --- EXECUTION (Playwright Power) ---

        // 1. Text Fields
        console.log("Filling Basic Info...");
        try { await page.locator('input[id="이름"]').fill(info.name); } catch(e) {}
        try { await page.locator('input[id="이메일"]').fill(info.email); } catch(e) {}
        try { await page.locator('input[name*="전화번호"]').fill(info.phone); } catch(e) {}

        // 2. Text Areas
        console.log("Filling Answers...");
        const textareas = await page.locator('textarea').all();
        if (textareas.length > 0) await textareas[0].fill(answers.q1);
        if (textareas.length > 1) await textareas[1].fill(answers.q2);

        // 3. File Upload
        console.log("Uploading File...");
        try {
            const fileInput = page.locator('input[type="file"]').first();
            await fileInput.setInputFiles(resumePath);
        } catch(e) { console.log("File upload failed:", e.message); }

        // 4. Checkboxes (Force Click)
        console.log("Clicking Agreements...");
        const checkboxes = await page.locator('input[type="checkbox"]').all();
        for (const box of checkboxes) {
            try {
                if (!(await box.isChecked())) {
                    await box.click({ force: true });
                    console.log("Checked a box.");
                }
            } catch(e) {}
        }

        console.log("\n✅ MISSION ACCOMPLISHED. Please review and submit.");

    } catch (error) {
        console.error("Execution Error:", error);
    } finally {
        if (browser) browser.close();
    }
}

executePerfectApply();
