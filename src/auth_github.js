import { chromium } from 'playwright';

async function openGitHubAuth() {
    console.log("🚀 Opening GitHub Login Page...");
    
    const browser = await chromium.launch({ 
        headless: false, 
        channel: 'chrome',
        args: ['--start-maximized'] 
    });
    
    const context = await browser.newContext({ viewport: null });
    const page = await context.newPage();
    
    // Direct link to Token Creation page (will ask for login first)
    await page.goto('https://github.com/settings/tokens/new?scopes=repo,delete_repo&description=Trae_Legacy_Cleanup', { waitUntil: 'networkidle' });

    console.log("👉 Please Log in and Generate Token (Scroll down -> Generate token).");
    console.log("👉 Copy the token (starts with ghp_...) and paste it here.");
    
    // Keep browser open
    await new Promise(() => {});
}

openGitHubAuth();
