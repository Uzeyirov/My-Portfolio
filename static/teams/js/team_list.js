document.addEventListener('DOMContentLoaded', function() {
    // Kartların sırayla gəlmə animasiyası
    const teamCards = document.querySelectorAll('.ms-team-card');
    teamCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Müraciət göndərən zaman düymənin vəziyyəti
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const form = modal.querySelector('form');
        const submitBtn = modal.querySelector('button[type="submit"]');
        
        if (form && submitBtn) {
            form.addEventListener('submit', function() {
                submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i>Göndərilir...';
                submitBtn.disabled = true;
            });
        }
    });
});