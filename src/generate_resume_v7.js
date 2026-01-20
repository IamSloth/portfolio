import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function generateFinalResumeV7() {
    console.log("Generating FINAL Resume V7 (A4 Optimized)...");
    
    // 1. Find Photo
    const assetsDir = path.resolve(__dirname, '../assets');
    const files = fs.readdirSync(assetsDir);
    const imageFiles = files.filter(f => ['.jpg', '.jpeg', '.png'].includes(path.extname(f).toLowerCase()));
    
    // Sort by modification time (Newest first)
    imageFiles.sort((a, b) => {
        return fs.statSync(path.join(assetsDir, b)).mtime.getTime() - 
               fs.statSync(path.join(assetsDir, a)).mtime.getTime();
    });
    
    const bestImage = imageFiles.length > 0 ? imageFiles[0] : 'profile_photo.jpg'; 
    console.log(`📸 Using Photo: ${bestImage}`);

    // 2. Load V7 Template & Inject Photo
    let htmlContent = fs.readFileSync(path.resolve(__dirname, 'resume_template_final_v7.html'), 'utf-8');
    const newSrc = `../assets/${bestImage}`;
    htmlContent = htmlContent.replace(/<img src="[^"]+" alt="임종권">/, `<img src="${newSrc}" alt="임종권">`);
    
    const tempHtmlPath = path.resolve(__dirname, 'resume_v7_temp.html');
    fs.writeFileSync(tempHtmlPath, htmlContent);

    // 3. Generate PDF
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    await page.goto(`file://${tempHtmlPath}`, { waitUntil: 'networkidle' });
    
    const pdfPath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume_Final_V7.pdf');
    
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' }
    });
    
    console.log(`✅ Resume V7 Generated: ${pdfPath}`);
    await browser.close();
}

generateFinalResumeV7();
