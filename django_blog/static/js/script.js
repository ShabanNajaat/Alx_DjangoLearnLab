// Django Blog JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Blog loaded successfully!');
    
    // Add any interactive functionality here
    const authForms = document.querySelectorAll('.auth-form');
    authForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.textContent = 'Processing...';
                submitBtn.disabled = true;
            }
        });
    });
});
