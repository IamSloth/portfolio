const fs = require('fs');
const text = fs.readFileSync('draft_v2_raw.txt', 'utf8');
const sections = text.split('===SECTION===');
sections.forEach((s, i) => {
  const trimmed = s.trim();
  if (trimmed) {
    console.log(`문항 ${i}: ${trimmed.length}자`);
  }
});
