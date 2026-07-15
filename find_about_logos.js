const fs = require('fs');
const content = fs.readFileSync('about.html', 'utf8');
const lines = content.split('\n');
lines.forEach((line, i) => {
    if (line.includes('seakfuel.png') || line.includes('steakfuel-tlogo.png')) {
        console.log(`Line ${i + 1}: ${line.trim()}`);
    }
});
