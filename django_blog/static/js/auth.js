// Authentication specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Authentication scripts loaded');
    
    // Form validation and enhancement
    const authForms = document.querySelectorAll('.auth-form');
    
    authForms.forEach(form => {
        // Add loading state to submit buttons
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('.auth-button');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = 'Processing...';
            }
        });
        
        // Real-time validation feedback
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
    
    function validateField(field) {
        const value = field.value.trim();
        const errorDiv = field.parentNode.querySelector('.error-message');
        
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                showError(field, 'Please enter a valid email address');
                return;
            }
        }
        
        if (field.required && !value) {
            showError(field, 'This field is required');
            return;
        }
        
        clearError(field);
    }
    
    function showError(field, message) {
        let errorDiv = field.parentNode.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        field.style.borderColor = '#dc3545';
    }
    
    function clearError(field) {
        const errorDiv = field.parentNode.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
        field.style.borderColor = '#ddd';
    }
});
