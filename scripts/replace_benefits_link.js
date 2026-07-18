const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        if (isDirectory) {
            walkDir(dirPath, callback);
        } else {
            callback(path.join(dir, f));
        }
    });
}

function processFile(filePath) {
    if (!filePath.endsWith('.html')) return;

    let content = fs.readFileSync(filePath, 'utf8');
    let newContent = content;
    
    // Replace the footer link (benefiits.html -> coming-soon.html)
    newContent = newContent.replace(/href="benefiits\.html"/g, 'href="coming-soon.html"');
    newContent = newContent.replace(/href="\.\.\/benefiits\.html"/g, 'href="../coming-soon.html"');
    newContent = newContent.replace(/href="\.\.\/\.\.\/benefiits\.html"/g, 'href="../../coming-soon.html"');

    // Replace the navbar link (href="#" -> correct href)
    let match = newContent.match(/href="([^"]*?)coming-soon\.html"[^>]*>Reviews<\/a>/);
    if (match) {
        let prefix = match[1]; // e.g. "", "../", "../../"
        newContent = newContent.replace(
            /<a href="#" (class="menu-link(?: red)?">Benefits<\/a>)/g,
            `<a href="${prefix}coming-soon.html" $1`
        );
    } else {
        // Fallback prefix extraction by looking at index.html link in menu
        let matchFallback = newContent.match(/href="([^"]*?)index\.html"[^>]*>Home<\/a>/);
        if (matchFallback) {
             let prefix = matchFallback[1];
             newContent = newContent.replace(
                /<a href="#" (class="menu-link(?: red)?">Benefits<\/a>)/g,
                `<a href="${prefix}coming-soon.html" $1`
            );
        }
    }

    if (newContent !== content) {
        fs.writeFileSync(filePath, newContent, 'utf8');
        console.log(`Updated: ${filePath}`);
    }
}

console.log("Starting link update...");
walkDir(process.cwd(), processFile);
console.log("Done.");
