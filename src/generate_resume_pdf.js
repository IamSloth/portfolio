const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

function generateResume() {
    const doc = new PDFDocument({ margin: 50 });
    const outputPath = path.join(__dirname, '../output/Lim_JongKwon_ShiftUp_Resume.pdf');
    
    doc.pipe(fs.createWriteStream(outputPath));

    // --- Header ---
    doc.fontSize(24).font('Helvetica-Bold').text('Lim Jong Kwon', { align: 'center' });
    doc.fontSize(10).font('Helvetica').text('Gwangmyeong-si, Gyeonggi-do | 010-4052-0834 | ssujklim@gmail.com', { align: 'center' });
    doc.moveDown();
    doc.moveTo(50, doc.y).lineTo(550, doc.y).stroke();
    doc.moveDown();

    // --- Summary ---
    doc.fontSize(14).font('Helvetica-Bold').text('Professional Summary');
    doc.fontSize(10).font('Helvetica').moveDown(0.5);
    doc.text(
        "Hybrid Operations Specialist with 6+ years of experience in General Affairs, Asset Management, and IT Support. " +
        "Uniquely qualified with an Electrical Engineering background (B.S.) for hardware troubleshooting and a Social Worker Certification (Level 1) for conflict resolution. " +
        "Proven track record of cost-cutting via in-house maintenance and process automation using AI tools. " +
        "Holder of Class 1 Large Driver's License (12 years accident-free). Eager to support Shift Up's creative environment."
    );
    doc.moveDown();

    // --- Skills ---
    doc.fontSize(14).font('Helvetica-Bold').text('Core Competencies');
    doc.fontSize(10).font('Helvetica').moveDown(0.5);
    doc.list([
        'IT Asset Management: PC/Server/Network H/W Troubleshooting & Lifecycle Management',
        'General Affairs: Facility Management, Vendor Negotiation, Cost Reduction',
        'Tools: ERP (Douzone/Ecount/Tibero), MS Office, Unity, ChatGPT (Automation)',
        'Soft Skills: Conflict Resolution, Stakeholder Communication (Tech-to-Biz Translation)'
    ]);
    doc.moveDown();

    // --- Experience ---
    doc.fontSize(14).font('Helvetica-Bold').text('Work Experience');
    doc.moveDown(0.5);

    // Job 1
    doc.fontSize(12).font('Helvetica-Bold').text('Social Solidarity Bank (Together Making World)', { continued: true });
    doc.fontSize(10).font('Helvetica').text('  |  Jan 2023 – Present', { align: 'right' });
    doc.text('General Affairs & IT Support Specialist');
    doc.fontSize(10).font('Helvetica').list([
        'Internalized IT infrastructure maintenance (L1/L2 troubleshooting), reducing outsourcing costs significantly.',
        'Managed ERP system migration and operation (Nexacro/Tibero), enabling data-driven decision making.',
        'Streamlined administrative workflows using AI tools, reducing documentation time by 80%.'
    ]);
    doc.moveDown();

    // Job 2
    doc.fontSize(12).font('Helvetica-Bold').text('MANZEON', { continued: true });
    doc.fontSize(10).font('Helvetica').text('  |  Mar 2020 – Nov 2021', { align: 'right' });
    doc.text('QA & Operations Associate (IoT Systems)');
    doc.fontSize(10).font('Helvetica').list([
        'Analyzed system logs to troubleshoot communication failures in IoT facility management systems.',
        'Conducted QA testing for control dashboards, ensuring UI/UX optimization for end-users.'
    ]);
    doc.moveDown();

    // Job 3
    doc.fontSize(12).font('Helvetica-Bold').text('EdgeCross', { continued: true });
    doc.fontSize(10).font('Helvetica').text('  |  May 2016 – Feb 2018', { align: 'right' });
    doc.text('Material Control & Purchasing Specialist');
    doc.fontSize(10).font('Helvetica').list([
        'Managed H/W manufacturing processes and BOM (Bill of Materials) with zero error rate.',
        'Designed PCB circuits and conducted soldering/prototyping, gaining deep H/W understanding.'
    ]);
    doc.moveDown();

    // --- Education ---
    doc.fontSize(14).font('Helvetica-Bold').text('Education');
    doc.moveDown(0.5);
    doc.fontSize(10).font('Helvetica').text('Soongsil University - Master of Social Welfare (2020)');
    doc.text('Soongsil University - B.S. in Electrical Engineering (2017)');
    doc.moveDown();

    // --- Certifications ---
    doc.fontSize(14).font('Helvetica-Bold').text('Certifications');
    doc.moveDown(0.5);
    doc.fontSize(10).font('Helvetica').list([
        'Certified Social Worker, Level 1 (Ministry of Health and Welfare)',
        'Driver License, Class 1 Large (12 years accident-free)'
    ]);

    doc.end();
    console.log(`Resume generated at: ${outputPath}`);
}

generateResume();
