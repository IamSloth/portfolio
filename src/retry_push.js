import { execSync } from 'child_process';
import path from 'path';

const WORK_DIR = path.resolve('temp_cleanup_workspace');

function retryPush() {
    console.log("🔄 Retrying Push with Larger Buffer...");
    
    try {
        // Increase Git Buffer
        execSync('git config http.postBuffer 524288000', { cwd: WORK_DIR }); // 500MB
        
        console.log("Pushing...");
        execSync('git push -u origin main', { cwd: WORK_DIR, stdio: 'inherit' });
        
        console.log("✅ Push Success!");
        
        // If success, trigger deletion part separately
        console.log("Now run: node src/run_delete_only.js");
        
    } catch (e) {
        console.error("❌ Push Failed Again:", e.message);
    }
}

retryPush();
