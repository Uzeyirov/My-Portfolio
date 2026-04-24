document.addEventListener('DOMContentLoaded', function() {
    // 1. Axtarış İnputu Effekti
    const searchInput = document.querySelector('.ms-search-input');
    const searchForm = document.querySelector('.ms-search-form');

    if (searchInput && searchForm) {
        // İnputa klikləyəndə formun kənarlarını neon rəngdə parlat
        searchInput.addEventListener('focus', () => {
            searchForm.style.boxShadow = '0 0 20px rgba(0, 209, 255, 0.2)';
            searchForm.style.borderColor = '#00D1FF';
        });

        searchInput.addEventListener('blur', () => {
            searchForm.style.boxShadow = 'none';
            searchForm.style.borderColor = 'rgba(0, 132, 255, 0.2)';
        });
    }

    // 2. Kartların yüklənmə animasiyası (Fade-in effect)
    const cards = document.querySelectorAll('.ms-solution-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.4s ease ${index * 0.1}s`;

        // Bir az gecikmə ilə kartları üzə çıxar
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    });

    // 3. Axtarış düyməsinə klikləyəndə kiçik bir "Loading" effekti
    const searchBtn = document.querySelector('.ms-btn-search');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            if (searchInput.value.trim() !== "") {
                this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            }
        });
    }
});