import { PDFDocument } from 'pdf-lib';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function mergeResumes() {
    console.log("🧬 Initiating FUSION Protocol (Sensitivity + Rationality)...");

    const outputDir = path.resolve(__dirname, '../../output');
    const assetsDir = path.resolve(__dirname, '../../assets/resumes');

    // 1. Load Source Files
    // The "Competitor's Emotional Cover Letter" (Assuming it's ShiftUp_Submission.pdf)
    // If not found, try the other one.
    let coverLetterPath = path.join(assetsDir, 'ShiftUp_Submission.pdf');
    if (!fs.existsSync(coverLetterPath)) {
        // Fallback to the other long one
        coverLetterPath = path.join(assetsDir, '[공대 출신] IT인프라·ERP 전문 6년차 경영지원 기술 조직 소통 & AI 업무혁신_deathbed0104.pdf');
    }
    
    // The "Trae's Rational Resume" (V7)
    const resumePath = path.join(outputDir, 'Lim_JongKwon_ShiftUp_Resume_Final_V7.pdf');

    if (!fs.existsSync(coverLetterPath) || !fs.existsSync(resumePath)) {
        console.error("❌ Source files missing!");
        return;
    }

    const coverPdfBytes = fs.readFileSync(coverLetterPath);
    const resumePdfBytes = fs.readFileSync(resumePath);

    // 2. Create New Document
    const mergedPdf = await PDFDocument.create();
    
    const coverPdf = await PDFDocument.load(coverPdfBytes);
    const resumePdf = await PDFDocument.load(resumePdfBytes);

    // 3. Extract & Merge
    // Take ONLY the 1st page of Cover Letter (The "Emotion" part)
    const [coverPage] = await mergedPdf.copyPages(coverPdf, [0]);
    mergedPdf.addPage(coverPage);

    // Take ALL pages of Resume (The "Logic" part) - usually 1 page
    const resumePages = await mergedPdf.copyPages(resumePdf, resumePdf.getPageIndices());
    for (const page of resumePages) {
        mergedPdf.addPage(page);
    }

    // 4. Save
    const fusionPath = path.join(outputDir, 'Lim_JongKwon_ShiftUp_Fusion_Resume.pdf');
    const mergedPdfBytes = await mergedPdf.save();
    fs.writeFileSync(fusionPath, mergedPdfBytes);

    console.log(`✅ FUSION COMPLETE: ${fusionPath}`);
    console.log("   [Page 1] Emotional Cover Letter");
    console.log("   [Page 2] Rational Impact Resume");
}

mergeResumes();
