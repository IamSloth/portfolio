import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function convertFinalHtmlToPdfV3() {
    console.log("Generating FINAL Design Resume (v3 with Local Image)...");
    
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    const htmlPath = path.resolve(__dirname, 'resume_template_final.html');
    const pdfPath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume_Design_v3.pdf');
    
    // Load HTML
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
    
    // Generate PDF
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' }
    });
    
    console.log(`✅ Final Resume Generated: ${pdfPath}`);
    await browser.close();
}

convertFinalHtmlToPdfV3();
