import axios from 'axios';

const TOKEN = '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';
const USER = 'IamSloth';
const REPO = 'LIM-PIPELINE';

async function deleteOneRepo() {
    console.log(`🗑️ Deleting ${REPO}...`);
    try {
        await axios.delete(`https://api.github.com/repos/${USER}/${REPO}`, {
            headers: { 
                'Authorization': `token ${TOKEN}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        });
        console.log(`✅ Deleted: ${REPO}`);
    } catch (e) {
        if (e.response && e.response.status === 404) {
            console.log(`⚠️ Already gone: ${REPO}`);
        } else {
            console.error(`❌ Failed to delete ${REPO}:`, e.message);
        }
    }
}

deleteOneRepo();
