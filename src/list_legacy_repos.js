import axios from 'axios';

async function listRepos() {
    const token = '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';
    
    try {
        const response = await axios.get('https://api.github.com/user/repos?type=owner&per_page=100', {
            headers: { 'Authorization': `token ${token}` }
        });
        
        const repos = response.data
            .filter(r => r.name !== 'Job-Application-Pipeline') // Exclude current project
            .map(r => r.name);
            
        console.log("--- CLEANUP TARGETS ---");
        console.log(repos.join('\n'));
        console.log(`\nTotal: ${repos.length} repositories found.`);
        
        // Save list for next step
        const fs = await import('fs');
        fs.writeFileSync('cleanup_list.json', JSON.stringify(repos));
        
    } catch (error) {
        console.error("Error:", error.message);
    }
}

listRepos();
