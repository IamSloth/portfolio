import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";
import dotenv from "dotenv";

dotenv.config();

async function run() {
  console.log("🤖 Starting Stagehand AI Agent (V2 Fix)...");

  const stagehand = new Stagehand({
    env: "LOCAL",
    verbose: 1,
    debugDom: true,
  });

  // Init returns an object containing the page in some versions, 
  // or sets it on the instance. Let's cover both.
  const initResult = await stagehand.init();
  const page = initResult.page || stagehand.page;

  if (!page) {
      throw new Error("❌ Failed to initialize Stagehand Page!");
  }

  console.log("🔗 Navigating to Smilegate...");
  await page.goto("https://careers.smilegate.com/apply/announce/view?seq=5759");

  console.log("🧠 AI: '지원하기' 버튼 찾아서 클릭해줘");
  
  try {
    await page.act({
      action: "click the '지원하기' button",
    });
    
    // Human-in-the-loop for Login
    console.log("\n🛑 [WAITING FOR USER LOGIN]");
    console.log("1. Please LOGIN manually in the browser window.");
    console.log("2. Navigate to the APPLICATION FORM page.");
    console.log("3. Press [ENTER] here when you see the form.");
    
    await new Promise(resolve => process.stdin.once('data', resolve));

    // Address Search via AI
    console.log("\n🧠 AI: 주소 검색 시작 (도덕로 79)");
    
    // Step 1: Click Search
    await page.act({
      action: "click the address search button (magnifying glass icon next to address input)",
    });
    
    await page.waitForTimeout(1000);

    // Step 2: Type Address
    // Stagehand is smart enough to find the input in the new modal/popup
    await page.act({
      action: "type '도덕로 79' into the address search input and press Enter",
    });

    await page.waitForTimeout(2000);

    // Step 3: Click Result
    await page.act({
      action: "click the first address result row",
    });

    console.log("✅ Address Filled via AI!");

  } catch (error) {
    console.error("❌ AI Error:", error);
  }
}

run();