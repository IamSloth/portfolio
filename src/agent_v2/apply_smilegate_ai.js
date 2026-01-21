import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";
import dotenv from "dotenv";

dotenv.config();

// 1. Stagehand 초기화 (Local Chrome 사용)
async function run() {
  console.log("🤖 Starting Stagehand AI Agent...");

  const stagehand = new Stagehand({
    env: "LOCAL", // 로컬 브라우저 사용
    verbose: 1,
    debugDom: true,
  });

  await stagehand.init();
  const page = stagehand.page;

  // 2. 이미 열려있는 페이지에 접속하거나 새로 이동
  // Stagehand는 기본적으로 새 브라우저를 띄웁니다.
  // 우리가 원하는 URL로 이동합니다.
  console.log("🔗 Navigating to Smilegate...");
  await page.goto("https://careers.smilegate.com/apply/announce/view?seq=5759");

  // 3. AI 기반 행동 수행 (Vision + DOM)
  console.log("🧠 AI: '지원하기' 버튼 찾아서 클릭해줘");
  
  try {
    // "지원하기" 버튼 클릭
    await page.act({
      action: "click the '지원하기' button",
    });
    
    // 로그인 페이지나 폼 페이지가 나올 때까지 대기
    await page.waitForTimeout(2000);

    // 4. 로그인 감지 및 처리 (Human-in-the-loop)
    // AI가 화면을 분석해서 '로그인'이 필요한지 판단
    const pageState = await page.extract({
      instruction: "Is this a login page? Return true if yes.",
      schema: z.object({ isLoginPage: z.boolean() }),
    });

    if (pageState.isLoginPage) {
      console.log("🛑 Login Required! Please login manually in the browser.");
      console.log("👉 After login, navigate to the application form.");
      console.log("👉 Press [ENTER] in this terminal when ready to continue.");
      
      // Node.js에서 사용자 입력 대기
      await new Promise(resolve => process.stdin.once('data', resolve));
    }

    // 5. 폼 입력 (주소 검색 포함)
    console.log("🧠 AI: 주소 검색 시작");
    
    // 주소 검색 버튼 클릭
    await page.act({
      action: "click the address search button (magnifying glass icon)",
    });

    // 팝업 대기
    await page.waitForTimeout(2000);

    // 팝업 내 검색어 입력 (Stagehand는 팝업/Iframe 자동 처리)
    await page.act({
      action: "type '도덕로 79' into the address search input and press Enter",
    });

    await page.waitForTimeout(2000);

    // 결과 클릭
    await page.act({
      action: "click the first address result that matches '도덕로 79'",
    });

    console.log("✅ Address Filled via AI!");

  } catch (error) {
    console.error("❌ AI Error:", error);
  } finally {
    // 브라우저 닫지 않음 (확인용)
    // await stagehand.close();
  }
}

run();