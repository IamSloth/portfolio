import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function generateFinalResumeV4() {
    console.log("Generating FINAL Resume V4 (Smart Photo Selection)...");
    
    // 1. Find the latest image file in assets
    const assetsDir = path.resolve(__dirname, '../assets');
    const files = fs.readdirSync(assetsDir);
    
    // Filter images
    const imageFiles = files.filter(f => ['.jpg', '.jpeg', '.png'].includes(path.extname(f).toLowerCase()));
    
    if (imageFiles.length === 0) {
        console.error("No image found in assets!");
        return;
    }

    // Sort by modification time (Newest first)
    imageFiles.sort((a, b) => {
        return fs.statSync(path.join(assetsDir, b)).mtime.getTime() - 
               fs.statSync(path.join(assetsDir, a)).mtime.getTime();
    });

    const bestImage = imageFiles[0];
    console.log(`📸 Selected Profile Photo: ${bestImage}`);

    // 2. Update HTML with the selected image
    let htmlContent = fs.readFileSync(path.resolve(__dirname, 'resume_template_final.html'), 'utf-8');
    
    // Replace the image src dynamically
    // Regex to find the img tag inside .profile-img
    const newSrc = `../assets/${bestImage}`;
    htmlContent = htmlContent.replace(/<img src="[^"]+" alt="임종권">/, `<img src="${newSrc}" alt="임종권">`);
    
    // Save to a temp HTML file for rendering
    const tempHtmlPath = path.resolve(__dirname, 'resume_v4_temp.html');
    fs.writeFileSync(tempHtmlPath, htmlContent);

    // 3. Generate PDF
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    await page.goto(`file://${tempHtmlPath}`, { waitUntil: 'networkidle' });
    
    const pdfPath = path.resolve(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume_Final.pdf');
    
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' }
    });
    
    console.log(`✅ Resume V4 Generated: ${pdfPath}`);
    await browser.close();
    
    // Cleanup
    // fs.unlinkSync(tempHtmlPath);
}

generateFinalResumeV4();
