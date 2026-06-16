const fs = require('fs');
const files = ['index.html', 'Time-Analysis.html', 'Category-Manager.html', 'Community-Insight.html', 'Reports-Export.html', 'Goals-Budgeting.html'];
let count=0;
files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    const regex = /<div class="flex items-center space-x-3 border-l pl-6 border-gray-200">\s*<div class="text-right leading-tight">\s*<p class="font-bold text-sm.*?">Architect Prime<\/p>\s*<p class=".*?">Pro Account<\/p>\s*<\/div>\s*<img src="https:\/\/i\.pravatar\.cc\/150\?u=a042581f4e29026704d" alt="Avatar" class=".*?">\s*<\/div>/g;
    
    if (regex.test(content)) {
        content = content.replace(regex, (match) => {
            count++;
            return match
                .replace('<div class="flex items-center space-x-3 border-l pl-6 border-gray-200">', '<a href="Profile.html" class="flex items-center space-x-3 border-l pl-6 border-gray-200 cursor-pointer hover:opacity-80 transition block">')
                .replace(/<\/div>$/, '</a>');
        });
        fs.writeFileSync(file, content);
    }
});
console.log('Replaced ' + count + ' occurrences.');
