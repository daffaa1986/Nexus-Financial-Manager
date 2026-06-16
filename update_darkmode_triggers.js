const fs = require('fs');

const files = [
    'index.html',
    'Time-Analysis.html',
    'Category-Manager.html',
    'Community-Insight.html',
    'Reports-Export.html',
    'Goals-Budgeting.html',
    'Settings.html',
    'Profile.html'
];

let count = 0;

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');

    const searchTarget = `<div class="text-[#64748B] cursor-pointer hover:text-slate-700 transition">
                            <!-- Toggle icon -->
                            <div class="w-5 h-5 rounded-full border-2 border-slate-400 flex overflow-hidden">
                                <div class="w-1/2 h-full bg-slate-400"></div>
                                <div class="w-1/2 h-full bg-transparent"></div>
                            </div>
                        </div>`;
                        
    const replacement = `<div class="dark-mode-toggle text-[#64748B] cursor-pointer hover:text-slate-700 transition" title="Toggle Dark Mode">
                            <!-- Toggle icon -->
                            <div class="w-5 h-5 rounded-full border-2 border-slate-400 flex overflow-hidden">
                                <div class="w-1/2 h-full bg-slate-400"></div>
                                <div class="w-1/2 h-full bg-transparent"></div>
                            </div>
                        </div>`;

    if (content.includes(searchTarget)) {
        content = content.replace(searchTarget, replacement);
        count++;
        fs.writeFileSync(file, content);
    }
});

console.log('Added dark-mode-toggle class to headers in ' + count + ' files.');
