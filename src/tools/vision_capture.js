import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// This tool is designed to be called by the MCP server or the Agent
// whenever a new application page is encountered.
// It captures a full-page screenshot for Visual Analysis.

async function captureForVision(url = null) {
    let browser;
    try {
        console.log("📸 Vision Tool: Initializing Capture...");
        
        // Connect to existing if possible, or launch new
        try {
            browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
        } catch (e) {
            browser = await chromium.launch();
        }

        const context = browser.contexts()[0] || await browser.newContext();
        const pages = context.pages();
        const page = pages.find(p => p.url().includes('career') || p.url().includes('recruit')) || pages[0];

        if (url) await page.goto(url);
        
        await page.waitForLoadState('networkidle');

        // Capture Full Page Screenshot
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `vision_capture_${timestamp}.png`;
        const filepath = path.resolve(__dirname, '../../output/vision_logs', filename);
        
        // Ensure dir exists
        const fs = await import('fs/promises');
        await fs.mkdir(path.dirname(filepath), { recursive: true });

        await page.screenshot({ path: filepath, fullPage: true });
        
        console.log(`✅ Screenshot Captured: ${filepath}`);
        console.log("-> Ready for AI Vision Analysis (to identify form layout and context).");

        return filepath;

    } catch (error) {
        console.error("❌ Vision Capture Failed:", error);
    } finally {
        if (browser && !browser.isConnected()) await browser.close();
    }
}

// Allow direct execution for testing
if (process.argv[1] === __filename) {
    captureForVision();
}

export { captureForVision };
