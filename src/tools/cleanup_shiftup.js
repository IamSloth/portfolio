import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '../../');

const sourceDir = path.join(rootDir, 'companies/shiftup');
const targetBaseDir = path.join(rootDir, 'companies/_submitted/shiftup');
const artifactsDir = path.join(targetBaseDir, 'artifacts');
const outputDir = path.join(rootDir, 'output');

console.log('🧹 Starting Cleanup for ShiftUp...');

// 1. Ensure Target Directories Exist
if (!fs.existsSync(targetBaseDir)) fs.mkdirSync(targetBaseDir, { recursive: true });
if (!fs.existsSync(artifactsDir)) fs.mkdirSync(artifactsDir, { recursive: true });

// 2. Move Script Files (companies/shiftup -> companies/_submitted/shiftup)
if (fs.existsSync(sourceDir)) {
    const files = fs.readdirSync(sourceDir);
    files.forEach(file => {
        const srcPath = path.join(sourceDir, file);
        const destPath = path.join(targetBaseDir, file);
        try {
            fs.renameSync(srcPath, destPath);
            console.log(`moved: ${file}`);
        } catch (e) {
            console.error(`Failed to move ${file}:`, e.message);
        }
    });
    
    // Remove empty source directory
    try {
        if (fs.readdirSync(sourceDir).length === 0) {
            fs.rmdirSync(sourceDir);
            console.log('Deleted empty folder: companies/shiftup');
        }
    } catch (e) {}
}

// 3. Move Artifacts (output/*ShiftUp* -> companies/_submitted/shiftup/artifacts)
if (fs.existsSync(outputDir)) {
    const outputFiles = fs.readdirSync(outputDir);
    outputFiles.forEach(file => {
        if (file.includes('ShiftUp') || file.includes('시프트업')) {
             const srcPath = path.join(outputDir, file);
             const destPath = path.join(artifactsDir, file);
             try {
                fs.renameSync(srcPath, destPath);
                console.log(`moved artifact: ${file}`);
             } catch (e) {
                 console.error(`Failed to move artifact ${file}:`, e.message);
             }
        }
    });
}

console.log('✅ Cleanup Completed successfully.');