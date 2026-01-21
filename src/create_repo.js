import axios from 'axios';

async function createRepo() {
    const token = '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';
    const repoName = 'Job-Application-Pipeline';
    
    console.log(`Creating Repository: ${repoName}...`);
    
    try {
        const response = await axios.post(
            'https://api.github.com/user/repos',
            {
                name: repoName,
                private: true, // Safety First!
                description: 'Automated Job Application System powered by Trae AI'
            },
            {
                headers: {
                    'Authorization': `token ${token}`,
                    'Accept': 'application/vnd.github.v3+json'
                }
            }
        );
        console.log("✅ Repository Created Successfully!");
        console.log("URL:", response.data.html_url);
    } catch (error) {
        console.error("❌ Failed to create repo:", error.response ? error.response.data : error.message);
    }
}

createRepo();
