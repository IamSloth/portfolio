import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function convertHtmlToPdf() {
    console.log("Generating High-Quality Design Resume...");
    
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    const htmlPath = path.resolve(__dirname, 'resume_template.html');
    const pdfPath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume_Design_v1.pdf');
    
    // Load local HTML file
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
    
    // Generate PDF
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true, // Print colors/backgrounds
        margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' } // Handled by CSS
    });
    
    console.log(`✅ Design Resume Generated: ${pdfPath}`);
    await browser.close();
}

convertHtmlToPdf();
