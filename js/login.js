document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginForm = document.getElementById('loginForm');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const eyeIcon = document.getElementById('eyeIcon');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');

    // Convenience pre-fill for development testing
    emailInput.value = 'architect@nexus.com';
    passwordInput.value = 'architect123';

    // Password Visibility Toggle
    if (togglePasswordBtn && eyeIcon && passwordInput) {
        togglePasswordBtn.addEventListener('click', function() {
            const isPassword = passwordInput.getAttribute('type') === 'password';
            passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
            
            // Toggle eye icon
            if (isPassword) {
                eyeIcon.classList.remove('fa-eye');
                eyeIcon.classList.add('fa-eye-slash');
            } else {
                eyeIcon.classList.remove('fa-eye-slash');
                eyeIcon.classList.add('fa-eye');
            }
        });
    }

    // Form validation and redirection to signup.html
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            let isValid = true;

            // Reset errors
            emailError.classList.add('hidden');
            passwordError.classList.add('hidden');
            emailInput.parentElement.classList.remove('border-red-500');
            passwordInput.parentElement.classList.remove('border-red-500');

            // Validate Email
            const emailValue = emailInput.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailValue) {
                emailError.textContent = 'Email address is required';
                emailError.classList.remove('hidden');
                emailInput.parentElement.classList.add('border-red-500');
                isValid = false;
            } else if (!emailRegex.test(emailValue)) {
                emailError.textContent = 'Please enter a valid email address';
                emailError.classList.remove('hidden');
                emailInput.parentElement.classList.add('border-red-500');
                isValid = false;
            }

            // Validate Password
            const passwordValue = passwordInput.value;
            if (!passwordValue) {
                passwordError.textContent = 'Password is required';
                passwordError.classList.remove('hidden');
                passwordInput.parentElement.classList.add('border-red-500');
                isValid = false;
            } else if (passwordValue.length < 6) {
                passwordError.textContent = 'Password must be at least 6 characters';
                passwordError.classList.remove('hidden');
                passwordInput.parentElement.classList.add('border-red-500');
                isValid = false;
            }

            // Redirect to Signup on Success
            if (isValid) {
                // Animate sign up button state
                const submitBtn = loginForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = `
                        <svg class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span>Loading Registration...</span>
                    `;
                }

                // Redirect to signup.html with pre-filled email
                setTimeout(() => {
                    window.location.href = `signup.html?email=${encodeURIComponent(emailValue)}`;
                }, 800);
            }
        });
    }

    // Request Access Button -> Logs in successfully
    const requestAccessBtn = document.getElementById('requestAccessBtn');
    if (requestAccessBtn) {
        requestAccessBtn.addEventListener('click', function() {
            localStorage.setItem('nexus_session', 'active_architect');
            requestAccessBtn.disabled = true;
            requestAccessBtn.innerHTML = `<i class="fas fa-spinner fa-spin mr-2"></i>Accessing...`;
            
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 800);
        });
    }

    // Social buttons login handlers
    const socialLogin = (btnId, spinnerColor) => {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.addEventListener('click', function() {
                localStorage.setItem('nexus_session', 'active_architect');
                btn.disabled = true;
                btn.innerHTML = `<i class="fas fa-spinner fa-spin text-sm ${spinnerColor}"></i>`;
                
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 800);
            });
        }
    };
    socialLogin('googleLoginBtn', 'text-amber-500');
    socialLogin('facebookLoginBtn', 'text-[#1877F2]');
    socialLogin('appleLoginBtn', 'text-[#131B2E]');

    // Dynamic bar chart loading animation
    const chartBars = document.querySelectorAll('.glass-card div.h-20 div');
    if (chartBars.length > 0) {
        // Clear heights initially
        const targetHeights = ['25%', '40%', '85%', '45%', '70%'];
        chartBars.forEach(bar => {
            bar.style.height = '0%';
        });

        // Animate up
        setTimeout(() => {
            chartBars.forEach((bar, index) => {
                bar.style.transition = 'height 1.2s cubic-bezier(0.4, 0, 0.2, 1)';
                bar.style.height = targetHeights[index];
            });
        }, 400);
    }
});
