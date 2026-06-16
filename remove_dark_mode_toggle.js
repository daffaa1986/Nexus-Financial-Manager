const fs = require('fs');

const files = [
    'index.html',
    'Time-Analysis.html',
    'Category-Manager.html',
    'Community-Insight.html',
    'Reports-Export.html',
    'Goals-Budgeting.html'
];
let count = 0;

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    
    // The exact HTML injected
    const toggleHtml = `<div class="dark-mode-toggle text-[#64748B] cursor-pointer hover:text-slate-700 transition" title="Toggle Dark Mode">
                        <!-- Toggle icon -->
                        <div class="w-5 h-5 rounded-full border-2 border-slate-400 flex overflow-hidden">
                            <div class="w-1/2 h-full bg-slate-400"></div>
                            <div class="w-1/2 h-full bg-transparent"></div>
                        </div>
                    </div>`;
                    
    const toggleHtmlAlt = `<div class="dark-mode-toggle text-[#64748B] cursor-pointer hover:text-slate-700 transition" title="Toggle Dark Mode">
                            <!-- Toggle icon -->
                            <div class="w-5 h-5 rounded-full border-2 border-slate-400 flex overflow-hidden">
                                <div class="w-1/2 h-full bg-slate-400"></div>
                                <div class="w-1/2 h-full bg-transparent"></div>
                            </div>
                        </div>`;

    // Strip out the dark-mode-toggle div using regex to ignore spacing differences
    const toggleRegex = /<div class="dark-mode-toggle[^>]+>\s*<!-- Toggle icon -->\s*<div class="w-5 h-5 rounded-full[^>]+>\s*<div class="w-1\/2 h-full bg-slate-400"><\/div>\s*<div class="w-1\/2 h-full bg-transparent"><\/div>\s*<\/div>\s*<\/div>\s*/;
    
    if (toggleRegex.test(content)) {
        content = content.replace(toggleRegex, '');
        fs.writeFileSync(file, content);
        count++;
    } else {
        console.log('Toggle not found in: ' + file);
    }
});
console.log('Removed toggle from ' + count + ' files.');
