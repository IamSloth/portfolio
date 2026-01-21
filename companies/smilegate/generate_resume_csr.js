import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../');

async function generateSmilegateResume() {
    console.log("Generating Smilegate CSR Specialized Resume...");
    
    // 1. Find Photo
    const assetsDir = path.resolve(projectRoot, 'assets');
    const files = fs.readdirSync(assetsDir);
    const imageFiles = files.filter(f => ['.jpg', '.jpeg', '.png'].includes(path.extname(f).toLowerCase()));
    
    // Sort by modification time (Newest first)
    imageFiles.sort((a, b) => {
        return fs.statSync(path.join(assetsDir, b)).mtime.getTime() - 
               fs.statSync(path.join(assetsDir, a)).mtime.getTime();
    });
    
    const bestImage = imageFiles.length > 0 ? imageFiles[0] : 'profile_photo.jpg'; 
    console.log(`📸 Using Photo: ${bestImage}`);

    // 2. Load Smilegate CSR Template & Inject Photo
    const templatePath = path.resolve(projectRoot, 'assets/templates/smilegate_csr_v1.html');
    let htmlContent = fs.readFileSync(templatePath, 'utf-8');
    
    // Adjust image path relative to temp file
    // Temp file will be in companies/smilegate/
    // Image is in assets/
    const newSrc = `../../assets/${bestImage}`;
    htmlContent = htmlContent.replace(/<img src="[^"]+" alt="임종권">/, `<img src="${newSrc}" alt="임종권">`);
    
    const companyDir = path.resolve(projectRoot, 'companies/smilegate');
    if (!fs.existsSync(companyDir)) fs.mkdirSync(companyDir, { recursive: true });

    const tempHtmlPath = path.join(companyDir, 'resume_csr_temp.html');
    fs.writeFileSync(tempHtmlPath, htmlContent);

    // 3. Generate PDF
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    await page.goto(`file://${tempHtmlPath}`, { waitUntil: 'networkidle' });
    
    const outputDir = path.resolve(projectRoot, 'output');
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

    const pdfPath = path.join(outputDir, 'Lim_JongKwon_Smilegate_CSR_Resume.pdf');
    
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' }
    });
    
    console.log(`✅ Resume Generated: ${pdfPath}`);
    await browser.close();
}

generateSmilegateResume();