const fs = require('fs');

const toggleHtml = `
                    <div class="dark-mode-toggle text-[#64748B] cursor-pointer hover:text-slate-700 transition" title="Toggle Dark Mode">
                        <!-- Toggle icon -->
                        <div class="w-5 h-5 rounded-full border-2 border-slate-400 flex overflow-hidden">
                            <div class="w-1/2 h-full bg-slate-400"></div>
                            <div class="w-1/2 h-full bg-transparent"></div>
                        </div>
                    </div>`;

function inject(file) {
    let content = fs.readFileSync(file, 'utf8');
    if (!content.includes('dark-mode-toggle')) {
        let parts = content.split('<a href="Settings.html"');
        if (parts.length > 1) {
            content = parts[0] + toggleHtml + '\n                    <a href="Settings.html"' + parts[1];
            fs.writeFileSync(file, content);
            console.log('Injected ' + file);
        } else {
            console.log('Could not find Settings link in ' + file);
        }
    } else {
        console.log(file + ' already has it');
    }
}

inject('Community-Insight.html');
inject('Reports-Export.html');

// For Settings.html, there is no settings link. We can add it next to the h2.
let settings = fs.readFileSync('Settings.html', 'utf8');
if (!settings.includes('dark-mode-toggle')) {
    let target = '<div class="mb-10">';
    let newHeader = `<div class="mb-10 flex justify-between items-start">
                <div>
                    <p class="text-[10px] text-gray-400 uppercase tracking-widest font-bold mb-1">ACCOUNT CONFIGURATION</p>
                    <h2 class="text-[32px] font-black text-[#0F172A] tracking-tight">System Settings</h2>
                </div>
                <!-- Toggle icon -->
                <div class="dark-mode-toggle mt-2 text-[#64748B] cursor-pointer hover:text-slate-700 transition" title="Toggle Dark Mode">
                    <div class="w-5 h-5 rounded-full border-2 border-slate-400 flex overflow-hidden">
                        <div class="w-1/2 h-full bg-slate-400"></div>
                        <div class="w-1/2 h-full bg-transparent"></div>
                    </div>
                </div>
            </div>`;
    
    // Replace the exact mb-10 div
    let oldHeadRegex = /<div class="mb-10">\s*<p[^>]+>ACCOUNT CONFIGURATION<\/p>\s*<h2[^>]+>System Settings<\/h2>\s*<\/div>/;
    if (oldHeadRegex.test(settings)) {
        settings = settings.replace(oldHeadRegex, newHeader);
        fs.writeFileSync('Settings.html', settings);
        console.log('Injected Settings.html');
    } else {
        console.log('Failed to match Settings.html header');
    }
} else {
    console.log('Settings.html already has it');
}
