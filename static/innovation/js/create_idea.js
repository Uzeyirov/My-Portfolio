document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('ideaForm');
    const submitBtn = form.querySelector('.btn-submit-glow');

    form.addEventListener('submit', function() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin me-2"></i> Yayımlanır...';
    });

    // Fayl seçiləndə kiçik bildiriş (opsional)
    const fileInput = document.querySelector('.custom-file-input');
    fileInput.addEventListener('change', function() {
        if (this.files[0]) {
            console.log("Fayl seçildi: " + this.files[0].name);
        }
    });
});