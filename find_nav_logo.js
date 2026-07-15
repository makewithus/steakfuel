const fs = require('fs');

const buffer = fs.readFileSync('index.html');
let content = buffer.toString('utf8');
if (buffer.length >= 2 && buffer[0] === 0xFF && buffer[1] === 0xFE) {
    content = buffer.slice(2).toString('utf16le');
}

const lines = content.split('\n');
lines.forEach((line, i) => {
    if (line.includes('nav-logo-header') || line.includes('footer-logo-image')) {
        console.log(`Line ${i + 1}: ${line.trim()}`);
    }
});
