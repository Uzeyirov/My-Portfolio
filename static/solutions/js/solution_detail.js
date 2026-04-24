/**
 * Şərhə cavab formunu açıb-bağlayan funksiya
 * @param {string} id - Şərhin ID-si
 */
function toggleReplyForm(id) {
    const form = document.getElementById('reply-form-' + id);
    if (form) {
        // Digər açıq formaları bağlamaq istəsən bura əlavə kod yazıla bilər
        form.classList.toggle('d-none');
        
        // Form açılanda avtomatik textarea-ya fokuslanmaq
        if (!form.classList.contains('d-none')) {
            const textarea = form.querySelector('textarea');
            if (textarea) textarea.focus();
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("Solution Detail səhifəsi hazırdır.");
    
    // Səs vermə düyməsinə kliklədikdə yükləmə effekti (opsional)
    const voteBtn = document.querySelector('form[action*="vote_solution"] button');
    if (voteBtn) {
        voteBtn.addEventListener('click', function() {
            this.style.opacity = "0.7";
        });
    }
});

// Şərhlərə cavab yazmaq üçün formun açılıb/bağlanması
function toggleReplyForm(commentId) {
    const formElement = document.getElementById('reply-form-' + commentId);
    if (formElement) {
        if (formElement.classList.contains('d-none')) {
            formElement.classList.remove('d-none');
        } else {
            formElement.classList.add('d-none');
        }
    }
}