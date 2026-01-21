import axios from 'axios';
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const TOKEN = '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';
const USER = 'IamSloth';
const ARCHIVE_NAME = 'Legacy-Archive-2025';
const WORK_DIR = path.resolve('temp_cleanup_workspace');

async function runCleanup() {
    console.log("🧹 Starting THE GREAT CLEANUP...");

    // 0. Prepare Workspace
    if (fs.existsSync(WORK_DIR)) fs.rmSync(WORK_DIR, { recursive: true, force: true });
    fs.mkdirSync(WORK_DIR);

    // 1. Create Archive Repo
    console.log(`Creating Archive Repo: ${ARCHIVE_NAME}...`);
    try {
        await axios.post('https://api.github.com/user/repos', {
            name: ARCHIVE_NAME,
            private: true,
            description: 'Archive of past projects (2016-2025)'
        }, { headers: { 'Authorization': `token ${TOKEN}` } });
    } catch (e) { console.log("Repo might already exist, proceeding..."); }

    // Initialize Local Git for Archive
    execSync('git init', { cwd: WORK_DIR });
    execSync(`git remote add origin https://${USER}:${TOKEN}@github.com/${USER}/${ARCHIVE_NAME}.git`, { cwd: WORK_DIR });

    // 2. Load Target List
    const targets = JSON.parse(fs.readFileSync('cleanup_list.json', 'utf-8'));
    
    console.log(`Found ${targets.length} targets to merge.`);

    // 3. Clone & Merge Loop
    for (const repo of targets) {
        console.log(`Processing: ${repo}...`);
        
        // Clone
        try {
            execSync(`git clone https://${TOKEN}@github.com/${USER}/${repo}.git`, { cwd: WORK_DIR, stdio: 'ignore' });
            
            // Remove .git folder to treat as simple files
            const repoPath = path.join(WORK_DIR, repo);
            fs.rmSync(path.join(repoPath, '.git'), { recursive: true, force: true });
            
        } catch (e) {
            console.error(`Failed to process ${repo}:`, e.message);
        }
    }

    // 4. Commit & Push Archive
    console.log("Pushing Archive to GitHub...");
    try {
        execSync('git add .', { cwd: WORK_DIR });
        execSync('git commit -m "Archive: Merged all legacy projects"', { cwd: WORK_DIR });
        execSync('git branch -M main', { cwd: WORK_DIR });
        execSync('git push -u origin main', { cwd: WORK_DIR });
        console.log("✅ Archive Uploaded Successfully!");
    } catch (e) {
        console.error("Push Failed:", e.message);
        return; // Stop if push fails (Safety)
    }

    // 5. DELETE Originals (The Scary Part)
    console.log("🗑️ Deleting Original Repos...");
    for (const repo of targets) {
        try {
            await axios.delete(`https://api.github.com/repos/${USER}/${repo}`, {
                headers: { 'Authorization': `token ${TOKEN}` }
            });
            console.log(`Deleted: ${repo}`);
        } catch (e) {
            console.error(`Failed to delete ${repo}:`, e.message);
        }
    }

    console.log("\n🎉 CLEANUP COMPLETE! Your GitHub is now pristine.");
    
    // Cleanup workspace
    // fs.rmSync(WORK_DIR, { recursive: true, force: true });
}

runCleanup();
