document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const fullNameInput = document.getElementById('fullName');
    const agreeTermsInput = document.getElementById('agreeTerms');
    const signupForm = document.getElementById('signupForm');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');
    const confirmPasswordError = document.getElementById('confirmPasswordError');

    // Parse URL parameters and pre-fill Email Address if passed
    const urlParams = new URLSearchParams(window.location.search);
    const emailParam = urlParams.get('email');
    if (emailParam && emailInput) {
        emailInput.value = decodeURIComponent(emailParam);
    }

    // Convenience pre-fill for development testing
    if (fullNameInput && emailInput && passwordInput && confirmPasswordInput && agreeTermsInput) {
        if (!emailInput.value) {
            emailInput.value = 'architect@nexus.com';
        }
        fullNameInput.value = 'Alexander Sterling';
        passwordInput.value = 'architect123';
        confirmPasswordInput.value = 'architect123';
        agreeTermsInput.checked = true;
    }

    // Form validation and signup handling
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            let isValid = true;

            // Reset errors
            emailError.classList.add('hidden');
            passwordError.classList.add('hidden');
            confirmPasswordError.classList.add('hidden');
            emailInput.parentElement.classList.remove('border-red-500');
            passwordInput.parentElement.classList.remove('border-red-500');
            confirmPasswordInput.parentElement.classList.remove('border-red-500');

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

            // Validate Confirm Password
            const confirmPasswordValue = confirmPasswordInput.value;
            if (!confirmPasswordValue) {
                confirmPasswordError.textContent = 'Please confirm your password';
                confirmPasswordError.classList.remove('hidden');
                confirmPasswordInput.parentElement.classList.add('border-red-500');
                isValid = false;
            } else if (passwordValue !== confirmPasswordValue) {
                confirmPasswordError.textContent = 'Passwords do not match';
                confirmPasswordError.classList.remove('hidden');
                confirmPasswordInput.parentElement.classList.add('border-red-500');
                isValid = false;
            }

            // Redirect to Dashboard on Success
            if (isValid) {
                localStorage.setItem('nexus_session', 'active_architect');
                
                // Animate button state
                const submitBtn = signupForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = `
                        <svg class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span>Creating Account...</span>
                    `;
                }

                // Redirect to dashboard after a delay
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
            }
        });
    }

    // Social buttons login handlers
    const socialSignup = (btnId, providerName, spinnerClass) => {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.addEventListener('click', function() {
                localStorage.setItem('nexus_session', 'active_architect');
                btn.disabled = true;
                btn.innerHTML = `<i class="fas fa-spinner fa-spin text-sm ${spinnerClass}"></i><span class="text-xs font-bold text-[#0F172A]">Loading...</span>`;
                
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
            });
        }
    };
    socialSignup('googleSignupBtn', 'Google', 'text-amber-500');
    socialSignup('facebookSignupBtn', 'Facebook', 'text-[#1877F2]');
    socialSignup('appleSignupBtn', 'Apple', 'text-[#131B2E]');

    // Dynamic bar chart loading animation
    const chartBars = document.querySelectorAll('.glass-card div.h-20 div, .glass-card div.h-24 div');
    if (chartBars.length > 0) {
        // Clear heights initially
        const targetHeights = ['30%', '45%', '35%', '85%', '50%'];
        chartBars.forEach(bar => {
            // Keep the peak-badge from getting squished or hidden by checking if bar doesn't contain a peak badge
            if (!bar.querySelector('.peak-badge')) {
                bar.style.height = '0%';
            }
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
