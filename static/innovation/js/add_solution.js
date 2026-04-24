document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('solutionForm');
    const submitBtn = form.querySelector('.btn-submit-glow');

    form.addEventListener('submit', function() {
        // Düyməni deaktiv et ki, ard-arda kliklənməsin
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Göndərilir...';
        
        // Bir az gecikmə (vizual effekt üçün, realda lazım deyil)
        setTimeout(() => {
            return true;
        }, 500);
    });

    // Fayl seçiləndə konsola məlumat yazmaq (və ya başqa vizual iş görmək üçün)
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                console.log(`Fayl seçildi: ${this.files[0].name}`);
            }
        });
    });
});