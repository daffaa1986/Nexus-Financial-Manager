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

    // Generate the standard structure with dynamic active classes
    let isSettingsActive = file === 'Settings.html';
    let isProfileActive = file === 'Profile.html';

    let settingsClass = isSettingsActive ? 'rounded-xl bg-[#1E3A8A]/30 text-blue-400' : 'hover:text-white';
    let settingsFont = isSettingsActive ? 'font-medium' : '';
    
    let profileClass = isProfileActive ? 'rounded-xl bg-[#1E3A8A]/30 text-blue-400' : 'hover:text-white';
    let profileFont = isProfileActive ? 'font-medium' : '';

    let newSidebarBottom = `<div class="mt-auto space-y-2 text-gray-400 pt-6 border-t border-slate-800">
                <a href="Settings.html" class="flex items-center space-x-3 p-3 ${settingsClass} transition">
                    <i class="fas fa-cog"></i>
                    <span class="${settingsFont}">Settings</span>
                </a>
                <a href="Profile.html" class="flex items-center space-x-3 p-3 ${profileClass} transition">
                    <i class="far fa-user"></i>
                    <span class="${profileFont}">Profile</span>
                </a>
            </div>
            
            <div class="mt-8 space-y-2 text-gray-400 text-sm">
                <a href="#" class="flex items-center space-x-3 hover:text-white transition">
                    <i class="far fa-question-circle"></i>
                    <span>Help Center</span>
                </a>
                <a href="#" class="flex items-center space-x-3 hover:text-white transition mt-4">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </div>
        </aside>`;
	
    // The trick is to replace everything from `<div class="mt-auto...` up to `</aside>`
    const regex = /<div class="mt-auto space-y-2 text-gray-400 pt-6 border-t border-slate-800">[\s\S]*?<\/aside>/;
    
    if (regex.test(content)) {
        content = content.replace(regex, newSidebarBottom);
        count++;
        fs.writeFileSync(file, content);
    }
});

console.log('Replaced sidebar bottom in ' + count + ' files.');
