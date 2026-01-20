const puppeteer = require('puppeteer-core');

async function debugFormStructure() {
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

        // 페이지의 모든 input, textarea 요소와 그 주변 정보를 싹 긁어옵니다.
        const formElements = await targetPage.evaluate(() => {
            const inputs = Array.from(document.querySelectorAll('input'));
            return inputs.map((el, index) => ({
                index: index,
                type: el.type,
                name: el.name,
                id: el.id,
                placeholder: el.placeholder,
                className: el.className,
                outerHTML: el.outerHTML, // 태그 전체 모양 확인
                parentText: el.parentElement ? el.parentElement.innerText : '' // 부모 요소의 텍스트(라벨일 가능성)
            }));
        });

        console.log("--- 감지된 INPUT 요소 목록 (정밀 분석) ---");
        console.log(JSON.stringify(formElements, null, 2));

    } catch (error) {
        console.error("DOM 분석 중 에러:", error);
    } finally {
        if (browser) browser.disconnect();
    }
}

debugFormStructure();
