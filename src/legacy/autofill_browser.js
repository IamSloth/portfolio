const puppeteer = require('puppeteer-core');

async function autoFillApplication() {
    let browser;
    try {
        browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });

        const pages = await browser.pages();
        let targetPage = null;

        // Find the application form tab
        for (const page of pages) {
            const url = page.url();
            if (url.includes('career.shiftup.co.kr') && url.includes('apply')) {
                targetPage = page;
                break;
            }
        }

        if (!targetPage) {
            console.log("Error: Could not find the application page tab.");
            return;
        }

        console.log(`Target Page Found: ${await targetPage.title()}`);
        await targetPage.bringToFront();

        // --- DATA PREPARATION ---
        const personalInfo = {
            name: "임종권",
            email: "ssujklim@gmail.com",
            phone: "010-4052-0834", 
            birth: "19920104", // Assuming birthdate format based on resume
            address: "경기도 광명시"
        };

        const answers = {
            motivation: `[게임 개발 환경의 안정성을 책임지는 'Tech-Savvy' 총무 전문가]
시프트업이 글로벌 게임 시장에서 혁신을 만들어가는 동안, 저는 그 혁신의 기반이 되는 임직원들의 업무 환경을 가장 안정적으로 지켜내고 싶습니다. 저는 단순한 자산 관리자가 아닙니다. 전기공학 전공 지식을 바탕으로 IT 자산의 하드웨어적 이슈를 직접 진단하고, 6년간의 총무 경력으로 자산 수명 주기(Life-cycle)를 체계적으로 관리해 온 '기술 기반 운영 전문가'입니다. 시프트업의 소중한 유무형 자산을 빈틈없이 관리하여 개발자분들이 오직 창작에만 몰입할 수 있는 최적의 환경을 제공하겠습니다.`,
            
            competency: `첫째, 개발자와 말이 통하는 하드웨어 트러블슈터입니다.
전기공학 학사 및 IoT 하드웨어 제조 경력을 보유하고 있어, PC/서버/네트워크 장비의 물리적 구조를 깊이 이해하고 있습니다. 단순 고장 접수 처리에 그치지 않고, 1차적으로 원인을 규명하고 해결하여 불필요한 외주 비용과 대기 시간을 획기적으로 줄일 수 있습니다.

둘째, 갈등을 해결하는 유연한 커뮤니케이션 능력입니다.
사회복지사 1급 자격을 통해 훈련된 공감 및 갈등 조정 능력으로 다양한 직군이 모인 게임사 조직 내에서 발생할 수 있는 요청 사항들을 원만하게 조율하겠습니다. 규정은 준수하되, 구성원의 입장을 배려하는 '해결 지향적' 지원을 약속드립니다.`,
            
            aspiration: `입사 즉시 보유하고 있는 자산 관리 노하우와 1종 대형 면허의 기동력을 활용하여 사옥 관리 및 임직원 지원 업무에 공백이 없도록 하겠습니다. 장기적으로는 시프트업의 자산 관리 프로세스를 데이터화하여 예산 낭비를 막고 효율을 극대화하는 스마트한 총무 시스템을 구축하겠습니다.`
        };

        // --- INJECTION LOGIC ---
        // Note: Selectors need to be generic or specific based on standard Korean recruit solutions (e.g., Greeting, Saramin, or custom)
        // Since we can't inspect the DOM interactively in this script easily, we use heuristics.
        
        console.log("Attempting to fill forms...");

        // 1. Name
        await tryType(targetPage, ['input[name*="name"]', 'input[id*="name"]', 'input[placeholder*="이름"]'], personalInfo.name);
        
        // 2. Email
        await tryType(targetPage, ['input[name*="email"]', 'input[id*="email"]', 'input[placeholder*="이메일"]'], personalInfo.email);
        
        // 3. Phone
        await tryType(targetPage, ['input[name*="phone"]', 'input[name*="mobile"]', 'input[id*="phone"]'], personalInfo.phone);

        // 4. Address (Often complex, skipping for now or doing partial)
        // await tryType(targetPage, ['input[name*="address"]'], personalInfo.address);

        // 5. Text Areas (Motivation, Self Intro)
        // Try to find textareas and fill them intelligently based on keywords in their labels
        const textareas = await targetPage.$$('textarea');
        console.log(`Found ${textareas.length} textareas.`);

        for (let i = 0; i < textareas.length; i++) {
            const el = textareas[i];
            // Check label or placeholder
            const placeholder = await targetPage.evaluate(e => e.getAttribute('placeholder'), el);
            const id = await targetPage.evaluate(e => e.getAttribute('id'), el);
            
            console.log(`Textarea ${i}: id=${id}, placeholder=${placeholder}`);

            if (i === 0) { // Usually the first one is Self Intro or Motivation
                 await el.type(answers.motivation + "\n\n" + answers.competency);
                 console.log("Filled Textarea 0 with Motivation/Competency");
            } else if (i === 1) {
                 await el.type(answers.aspiration);
                 console.log("Filled Textarea 1 with Aspiration");
            }
        }

        console.log("\n✅ Auto-fill process completed (Guardrails active: Submit button NOT pressed).");
        console.log("Please review the browser window.");

    } catch (error) {
        console.error("Error during auto-fill:", error);
    } finally {
        if (browser) browser.disconnect();
    }
}

async function tryType(page, selectors, value) {
    for (const selector of selectors) {
        try {
            const element = await page.$(selector);
            if (element) {
                await element.type(value);
                console.log(`Filled ${selector} with "${value}"`);
                return;
            }
        } catch (e) { /* ignore */ }
    }
    console.log(`Failed to find field for: ${value} (Selectors: ${selectors.join(', ')})`);
}

autoFillApplication();
