import axios from 'axios';
import fs from 'fs';

const TOKEN = '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';
const USER = 'IamSloth';

async function deleteLegacyRepos() {
    console.log("🔥 Starting THE GREAT PURGE...");
    
    // List from previous step + the failed archive repo
    const targets = JSON.parse(fs.readFileSync('cleanup_list.json', 'utf-8'));
    targets.push('Legacy-Archive-2025'); // Add the temp archive repo
    
    let deletedCount = 0;

    for (const repo of targets) {
        console.log(`Deleting: ${repo}...`);
        try {
            await axios.delete(`https://api.github.com/repos/${USER}/${repo}`, {
                headers: { 
                    'Authorization': `token ${TOKEN}`,
                    'Accept': 'application/vnd.github.v3+json'
                }
            });
            console.log(`✅ Deleted: ${repo}`);
            deletedCount++;
        } catch (e) {
            if (e.response && e.response.status === 404) {
                console.log(`⚠️ Already gone: ${repo}`);
            } else {
                console.error(`❌ Failed to delete ${repo}:`, e.message);
            }
        }
    }

    console.log(`\n🎉 PURGE COMPLETE! Deleted ${deletedCount} repositories.`);
    console.log("Your GitHub is now fresh and clean.");
}

deleteLegacyRepos();
