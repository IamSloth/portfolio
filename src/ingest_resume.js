const fs = require('fs');
const path = require('path');
const pdf = require('pdf-parse');

const resumeDir = path.join(__dirname, '../assets/resumes');
const outputFile = path.join(__dirname, '../assets/Master_Resume_Source.md');

async function ingestResumes() {
    try {
        const files = fs.readdirSync(resumeDir);
        let masterContent = "# Master Resume Source\n\nGenerated on: " + new Date().toISOString() + "\n\n";

        console.log(`Found ${files.length} files in ${resumeDir}`);

        for (const file of files) {
            if (file.toLowerCase().endsWith('.pdf')) {
                console.log(`Processing: ${file}`);
                const filePath = path.join(resumeDir, file);
                const dataBuffer = fs.readFileSync(filePath);
                
                try {
                    const data = await pdf(dataBuffer);
                    
                    masterContent += `\n\n---\n# SOURCE FILE: ${file}\n---\n\n`;
                    // Clean up some common PDF parsing artifacts if necessary, 
                    // but keeping it raw is safer for now to avoid losing info.
                    masterContent += data.text; 
                    
                } catch (err) {
                    console.error(`Error parsing ${file}:`, err);
                    masterContent += `\n\n---\n# ERROR READING FILE: ${file}\n---\n${err.message}\n`;
                }
            } else {
                console.log(`Skipping non-PDF file: ${file}`);
            }
        }

        fs.writeFileSync(outputFile, masterContent);
        console.log(`\nSuccessfully created Master Resume Source at: ${outputFile}`);
        
    } catch (error) {
        console.error("Critical error during ingestion:", error);
    }
}

ingestResumes();
