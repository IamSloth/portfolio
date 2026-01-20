const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

function generateKoreanResume() {
    const doc = new PDFDocument({ margin: 50, size: 'A4' });
    const outputPath = path.join(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume_KR.pdf');
    
    // Use system font for Korean support
    const fontPath = 'C:\\Windows\\Fonts\\malgun.ttf'; 
    
    // If malgun doesn't exist (rare), fallback to another or error nicely
    try {
        doc.font(fontPath);
    } catch (e) {
        console.error("Font not found. Please ensure Malgun Gothic is installed.");
        return;
    }

    doc.pipe(fs.createWriteStream(outputPath));

    // --- Header ---
    doc.fontSize(24).text('임 종 권 (Lim Jong Kwon)', { align: 'center' });
    doc.fontSize(11).text('경기도 광명시 거주 | 010-4052-0834 | ssujklim@gmail.com', { align: 'center' });
    doc.moveDown(0.5);
    
    // Draw Line
    doc.moveTo(50, doc.y).lineTo(545, doc.y).stroke();
    doc.moveDown(1);

    // --- Core Competency (핵심 역량) ---
    doc.fontSize(16).text('[핵심 역량: 기술과 사람을 잇는 하이브리드 전문가]');
    doc.fontSize(11).moveDown(0.5);
    doc.text(`• 전기공학(학사) 베이스: IT 자산(PC/서버/네트워크)의 하드웨어적 구조를 이해하고 직접 트러블슈팅 가능 (단순 관리자 아님)`);
    doc.text(`• 사회복지사 1급(석사): 조직 내 다양한 직군 간의 갈등을 중재하고, 임직원의 고충을 세심하게 케어하는 커뮤니케이션 스킬`);
    doc.text(`• 실무형 총무: 1종 대형 면허 보유 (12년 무사고) 및 자산 관리/구매/시설 관리 6년 경력`);
    doc.text(`• 업무 혁신: ERP(더존/이카운트) 도입 주도 및 AI 도구(ChatGPT)를 활용한 행정 업무 자동화 경험`);
    doc.moveDown(1.5);

    // --- Work Experience (경력 기술) ---
    doc.fontSize(16).text('경력 사항 (Total 6년 8개월)');
    doc.moveDown(0.5);

    // Job 1
    doc.fontSize(13).text('(사)함께만드는세상 | 전산총무 및 IT 지원 (2023.01 – 재직중)');
    doc.fontSize(11).text('  - IT 인프라 내재화: 네트워크/PC 장애 발생 시 L1/L2 수준 직접 해결 (유지보수 외주 비용 30% 절감)');
    doc.text('  - 자산 관리 체계화: 입/퇴사자 장비 지급 프로세스 정립 및 유휴 장비 재배치로 중복 구매 방지');
    doc.text('  - ERP 도입/운영: 커스텀 ERP(Nexacro) 구축 PM 수행 및 데이터 마이그레이션 주도');
    doc.moveDown(1);

    // Job 2
    doc.fontSize(13).text('(주)맨지온 | IoT 시스템 운영 및 QA (2020.03 – 2021.11)');
    doc.fontSize(11).text('  - 트러블슈팅: 시설 관제 시스템 통신 로그 분석을 통해 하드웨어/SW 귀책 사유 규명');
    doc.text('  - QA 품질 관리: 사용자(User) 관점의 UI/UX 테스트 수행으로 운영 효율성 증대');
    doc.moveDown(1);

    // Job 3
    doc.fontSize(13).text('(주)엣지크로스 | 자재 관리 및 구매 (2016.05 – 2018.02)');
    doc.fontSize(11).text('  - 하드웨어 이해: PCB 회로 설계 및 납땜 경험을 통해 전자기기 작동 원리 완벽 이해');
    doc.text('  - 자산(BOM) 관리: 제조 원가 절감을 위한 자재 소싱 및 재고 오차율 0% 달성');
    doc.moveDown(1.5);

    // --- Education (학력) ---
    doc.fontSize(16).text('학력 사항');
    doc.moveDown(0.5);
    doc.fontSize(11).text('• 숭실대학교 사회복지대학원 석사 졸업 (2020.02) - 사회적기업/갈등해결 전공');
    doc.text('• 숭실대학교 공과대학 전기공학부 학사 졸업 (2017.02)');
    doc.moveDown(1.5);

    // --- Certifications (자격 및 기타) ---
    doc.fontSize(16).text('자격 및 스킬');
    doc.moveDown(0.5);
    doc.fontSize(11).text('• 자격증: 사회복지사 1급 (보건복지부), 1종 대형 운전면허 (경찰청)');
    doc.text('• Tools: Unity/C# (게임 개발 프로세스 이해), MS Office (Expert), Notion, Slack');
    
    doc.end();
    console.log(`Korean Resume generated at: ${outputPath}`);
}

generateKoreanResume();
