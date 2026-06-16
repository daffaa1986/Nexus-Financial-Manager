const fs = require('fs');

const files = [
    'index.html',
    'Time-Analysis.html',
    'Category-Manager.html',
    'Community-Insight.html',
    'Reports-Export.html',
    'Goals-Budgeting.html',
    'Settings.html'
];
let count = 0;

const toggleHtml = `
                    <div class="dark-mode-toggle text-[#64748B] cursor-pointer hover:text-slate-700 transition" title="Toggle Dark Mode">
                        <!-- Toggle icon -->
                        <div class="w-5 h-5 rounded-full border-2 border-slate-400 flex overflow-hidden">
                            <div class="w-1/2 h-full bg-slate-400"></div>
                            <div class="w-1/2 h-full bg-transparent"></div>
                        </div>
                    </div>`;

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    // Ensure we don't duplicate
    if (!content.includes('dark-mode-toggle')) {
        // Regex to match the entire bell div block safely
        // Example:
        // <div class="relative text-gray-500 cursor-pointer">
        //     <i class="far fa-bell text-xl"></i>
        //     <span class="absolute -top-1 -right-0.5 w-2 h-2 bg-red-500 rounded-full border-2 border-[#FAF8FF]"></span>
        // </div>
        let bellRegex = /(<div class="relative text-[^>]+ cursor-pointer">\s*<i class="far fa-bell[^>]+><\/i>\s*(?:<span class="[^>]+><\/span>\s*)?<\/div>)/i;
        
        if (bellRegex.test(content)) {
            content = content.replace(bellRegex, '$1' + toggleHtml);
            fs.writeFileSync(file, content);
            count++;
        } else {
            console.log('FAILED to match bell icon in: ' + file);
        }
    } else {
        console.log(file + ' already has dark-mode-toggle');
    }
});
console.log('Injected toggle icon into ' + count + ' files.');
