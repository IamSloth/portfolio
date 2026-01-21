import { execSync } from 'child_process';
import path from 'path';

const WORK_DIR = path.resolve('temp_cleanup_workspace');

function forceCommitPush() {
    console.log("💪 Force Committing...");
    
    try {
        // Increase Git Buffer first
        execSync('git config http.postBuffer 524288000', { cwd: WORK_DIR });

        // Add (might take time)
        console.log("Adding files...");
        execSync('git add .', { cwd: WORK_DIR });
        
        // Commit
        console.log("Committing...");
        execSync('git commit -m "Archive: Merged all legacy projects"', { cwd: WORK_DIR });
        
        // Branch
        execSync('git branch -M main', { cwd: WORK_DIR });
        
        // Push
        console.log("Pushing...");
        execSync('git push -u origin main', { cwd: WORK_DIR, stdio: 'inherit' });
        
        console.log("✅ Success! Now deleting originals...");
        
        // Call delete script
        // execSync('node src/run_delete_only.js', { stdio: 'inherit' });
        
    } catch (e) {
        console.error("❌ Failed:", e.message);
    }
}

forceCommitPush();
