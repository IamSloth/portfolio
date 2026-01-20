import { chromium } from 'playwright';

async function inspectQuestions() {
    // Connect to the EXISTING demo window (port 9222 or finding the process)
    // Since we launched a new browser in demo_window.js, we can't easily connect to it unless we opened it with debugging port.
    // But demo_window.js didn't open with debugging port. My mistake.
    
    // I will use the MCP server (which is running on terminal 3 and connected to the FIRST browser) 
    // OR just launch a headless inspector to the URL again to read the questions.
    // To be safe and fast, let's just visit the URL in headless mode and SCRAPE the questions text.
    
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto('https://career.shiftup.co.kr/ko/o/78188/apply');

    // Scrape Labels/Questions associated with textareas
    const questions = await page.evaluate(() => {
        const textareas = document.querySelectorAll('textarea');
        return Array.from(textareas).map((el, index) => {
            // Find the closest preceding header or label
            // Shift Up uses styled divs usually. Let's look at the parent structure.
            let container = el.parentElement;
            let questionText = "Unknown";
            
            // Traverse up to find the question block
            // Usually: <div> <p>Question</p> <textarea>...
            while (container && container.innerText.length < 200) { // Limit traversal
                if (container.innerText.includes('?')) {
                   // This container probably has the question
                   questionText = container.innerText.split('\n')[0]; // First line often
                   break;
                }
                // Or look for specific class names if known, but generic is safer
                const siblings = container.parentElement ? Array.from(container.parentElement.children) : [];
                const myIndex = siblings.indexOf(container);
                if (myIndex > 0) {
                    const prev = siblings[myIndex - 1];
                    if (prev) {
                        questionText = prev.innerText;
                        break;
                    }
                }
                container = container.parentElement;
            }
            
            // Fallback: Just get placeholder
            if (questionText === "Unknown") {
                questionText = el.placeholder || "No Placeholder";
            }

            return { index, question: questionText.trim() };
        });
    });

    console.log("--- FOUND QUESTIONS ---");
    console.log(JSON.stringify(questions, null, 2));
    
    await browser.close();
}

inspectQuestions();
