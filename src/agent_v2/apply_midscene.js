import { PuppeteerAgent } from '@midscene/web';
import puppeteer from 'puppeteer';

(async () => {
  console.log("🤖 Starting Midscene AI Agent...");

  // 1. Launch Browser
  const browser = await puppeteer.launch({
    headless: false, // Visible
    args: ['--start-maximized'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });

  // 2. Initialize Midscene Agent
  const agent = new PuppeteerAgent(page);

  // 3. Navigate
  console.log("🔗 Navigating...");
  await page.goto("https://careers.smilegate.com/apply/announce/view?seq=5759");

  // 4. AI Action: Click Apply
  console.log("🧠 AI: '지원하기' 클릭");
  await agent.aiAction('Click the "지원하기" button');

  // Human Login Wait
  console.log("\n🛑 [WAITING FOR USER LOGIN]");
  console.log("Please login and go to the form page.");
  console.log("Press [ENTER] here when ready.");
  await new Promise(resolve => process.stdin.once('data', resolve));

  // 5. AI Action: Address Search
  console.log("🧠 AI: 주소 검색 (도덕로 79)");
  
  // "주소 검색 아이콘을 누르고, 팝업이 뜨면 '도덕로 79'를 입력하고 엔터를 쳐줘"
  // Midscene은 긴 명령도 이해합니다.
  await agent.aiAction(`
    1. Click the magnifying glass icon next to "주소" input.
    2. Wait for the popup.
    3. Type "도덕로 79" in the search input inside the popup.
    4. Press Enter.
    5. Click the first address result in the list.
  `);

  console.log("✅ Address Filled via Midscene!");

})();