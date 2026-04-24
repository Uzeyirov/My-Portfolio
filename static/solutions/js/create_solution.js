document.addEventListener('DOMContentLoaded', function() {
    const createForm = document.querySelector('.ms-form');
    const submitBtn = document.querySelector('.ms-btn-primary');

    if (createForm) {
        createForm.addEventListener('submit', function() {
            // Düymənin içinə loading ikon qoyur ki, yükləndiyini bilsin (xüsusilə şəkil/pdf atanda)
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i>Yüklenir...';
        });
    }

    // Fayl seçiləndə inputun rəngini dəyişmək üçün (vizual effekt)
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                this.style.borderColor = '#00D1FF';
                this.style.backgroundColor = 'rgba(0, 209, 255, 0.05)';
            }
        });
    });
});