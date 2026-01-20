import fs from 'fs';
import path from 'path';
import pdf from 'pdf-parse/lib/pdf-parse.js';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function compareResumes() {
    const dir = path.resolve(__dirname, '../assets/resumes');
    
    const fileA = path.join(dir, 'Lim_JongKwon_ShiftUp_Resume_Final_V7.pdf');
    const fileB = path.join(dir, '[공대 출신] IT인프라·ERP 전문 6년차 경영지원 기술 조직 소통 & AI 업무혁신_deathbed0104.pdf');
    
    console.log("📄 Reading File A (Trae V7)...");
    const dataA = await pdf(fs.readFileSync(fileA));
    
    console.log("📄 Reading File B (Competitor)...");
    const dataB = await pdf(fs.readFileSync(fileB));
    
    return {
        A: { text: dataA.text, pages: dataA.numpages },
        B: { text: dataB.text, pages: dataB.numpages }
    };
}

compareResumes().then(result => {
    console.log("--- ANALYSIS START ---");
    console.log(`[File A] Length: ${result.A.text.length} chars, Pages: ${result.A.pages}`);
    console.log(`[File B] Length: ${result.B.text.length} chars, Pages: ${result.B.pages}`);
    console.log("\n[File A Content Snippet]:\n", result.A.text.substring(0, 300));
    console.log("\n[File B Content Snippet]:\n", result.B.text.substring(0, 300));
    console.log("--- ANALYSIS END ---");
});
