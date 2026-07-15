const fs = require('fs');
const path = require('path');

const newFooterLogo = '<img loading="lazy" src="images/seakfuel.png" alt="STEAK FUEL brand logo." class="footer-logo-image">';

function processDir(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            processDir(fullPath);
        } else if (fullPath.endsWith('.html')) {
            const buffer = fs.readFileSync(fullPath);
            let encoding = 'utf8';
            let content = '';
            
            if (buffer.length >= 2 && buffer[0] === 0xFF && buffer[1] === 0xFE) {
                encoding = 'utf16le';
                content = buffer.slice(2).toString('utf16le');
            } else if (buffer.length >= 2 && buffer[0] === 0xFE && buffer[1] === 0xFF) {
                encoding = 'utf16be';
                content = buffer.slice(2).toString('utf16be');
            } else {
                content = buffer.toString('utf8');
            }
            
            const originalContent = content;

            // Replace footer logo
            content = content.replace(/<img[^>]*?class="footer-logo-image"[^>]*?>/g, newFooterLogo);

            if (content !== originalContent) {
                if (encoding === 'utf16le') {
                    const bom = Buffer.from([0xFF, 0xFE]);
                    const strBuf = Buffer.from(content, 'utf16le');
                    fs.writeFileSync(fullPath, Buffer.concat([bom, strBuf]));
                } else if (encoding === 'utf16be') {
                    const bom = Buffer.from([0xFE, 0xFF]);
                    const strBuf = Buffer.from(content, 'utf16be');
                    fs.writeFileSync(fullPath, Buffer.concat([bom, strBuf]));
                } else {
                    fs.writeFileSync(fullPath, content, 'utf8');
                }
                console.log('Updated footer logo in:', fullPath);
            }
        }
    }
}

processDir('.');
console.log('Footer logo replacement complete.');
