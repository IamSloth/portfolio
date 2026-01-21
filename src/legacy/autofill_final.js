const puppeteer = require('puppeteer-core');

async function autoFillFinal() {
    let browser;
    try {
        browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });

        const pages = await browser.pages();
        let targetPage = null;

        for (const page of pages) {
            const url = page.url();
            if (url.includes('career.shiftup.co.kr') && url.includes('apply')) {
                targetPage = page;
                break;
            }
        }

        if (!targetPage) {
            console.log("페이지를 못 찾았습니다.");
            return;
        }

        console.log(`Target Page: ${await targetPage.title()}`);
        await targetPage.bringToFront();

        const personalInfo = {
            name: "임종권",
            email: "ssujklim@gmail.com",
            phone: "01040520834" // 하이픈 제거 요구사항 반영
        };

        console.log("--- 2차 시도: 한글 ID 타겟팅 입력 ---");

        // 1. 이름 입력
        // id="이름"
        try {
            await targetPage.type('input[id="이름"]', personalInfo.name);
            console.log("✅ 이름 입력 완료");
        } catch (e) { console.log("❌ 이름 입력 실패"); }

        // 2. 이메일 입력
        // id="이메일"
        try {
            await targetPage.type('input[id="이메일"]', personalInfo.email);
            console.log("✅ 이메일 입력 완료");
        } catch (e) { console.log("❌ 이메일 입력 실패"); }

        // 3. 전화번호 입력
        // id="전화번호('-' 없이 입력해 주세요)" -> 특수문자가 포함된 ID는 escape 처리 필요
        try {
            // CSS selector로 특수문자 id를 잡으려면 escape가 복잡하므로, 속성 선택자 사용
            await targetPage.type('input[name*="전화번호"]', personalInfo.phone);
            console.log("✅ 전화번호 입력 완료");
        } catch (e) { console.log("❌ 전화번호 입력 실패", e); }


        console.log("\n--- 기본 정보 입력 완료. 브라우저 확인 요망 ---");

    } catch (error) {
        console.error("실행 중 에러:", error);
    } finally {
        if (browser) browser.disconnect();
    }
}

autoFillFinal();
