document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.ms-neon-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    const inputs = form.querySelectorAll('.form-control, .ms-textarea');

    // 1. Input Focus Effekti (Giriş animasiyası)
    inputs.forEach((input, index) => {
        input.style.opacity = '0';
        input.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            input.style.transition = 'all 0.5s ease';
            input.style.opacity = '1';
            input.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });

    // 2. "Kimləri axtarırsan?" bölməsi üçün dinamik ipucu
    const lookingForInput = document.querySelector('input[name="looking_for"]');
    if (lookingForInput) {
        lookingForInput.addEventListener('input', function(e) {
            // Əgər istifadəçi vergül qoyursa, balaca bir parlama effekti verək
            if (e.data === ',') {
                this.parentElement.style.boxShadow = '0 0 15px rgba(0, 209, 255, 0.4)';
                setTimeout(() => {
                    this.parentElement.style.boxShadow = 'none';
                }, 500);
            }
        });
    }

    // 3. Form Göndəriləndə "Loading" (Yüklənir) halı
    form.addEventListener('submit', function() {
        // Düymənin daxilini dəyişək
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            KOMANDA QURULUR...
        `;
        submitBtn.style.letterSpacing = '3px';
        submitBtn.style.opacity = '0.8';
        
        // Kiçik bir vizual vibe: Formanı bir az şəffaflaşdıraq
        form.style.transition = 'opacity 0.5s ease';
        form.style.opacity = '0.5';
    });

    // 4. Input-ların boş qalmaması üçün sürətli yoxlama (Real-time Validation)
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === "" && this.hasAttribute('required')) {
                this.parentElement.style.borderColor = '#ff4b2b'; // Səhv halında qırmızımtıl neon
            } else {
                this.parentElement.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            }
        });
    });
});