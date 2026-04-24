// Cavab formasını açıb-bağlayan funksiya
function toggleReplyForm(commentId) {
    const form = document.getElementById(`reply-form-${commentId}`);
    if (form) {
        // Əvvəlcə bütün digər cavab formalarını bağla
        document.querySelectorAll('[id^="reply-form-"]').forEach(el => {
            if (el.id !== `reply-form-${commentId}`) {
                el.classList.add('d-none');
            }
        });

        // Seçilən formanı aç və ya bağla
        form.classList.toggle('d-none');
        
        // Əgər açılıbsa, dərhal inputa fokuslan
        if (!form.classList.contains('d-none')) {
            const input = form.querySelector('input[type="text"]');
            if (input) input.focus();
        }
    }
}

// Səsvermə düyməsinə kliklədikdə kiçik bir "click" effekti
const voteBtn = document.querySelector('.ms-vote-btn');
if (voteBtn) {
    voteBtn.addEventListener('mousedown', () => {
        voteBtn.style.transform = 'scale(0.9)';
    });
    voteBtn.addEventListener('mouseup', () => {
        voteBtn.style.transform = 'scale(1)';
    });
}