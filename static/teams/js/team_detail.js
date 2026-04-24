document.addEventListener('DOMContentLoaded', function() {
    // Səhifə elementlərinin yumşaq şəkildə açılması
    const mainCard = document.querySelector('.ms-main-card');
    const sidebars = document.querySelectorAll('.ms-sidebar-card');

    if (mainCard) {
        mainCard.style.opacity = '0';
        mainCard.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            mainCard.style.transition = 'all 0.6s ease';
            mainCard.style.opacity = '1';
            mainCard.style.transform = 'translateX(0)';
        }, 100);
    }

    sidebars.forEach((side, index) => {
        side.style.opacity = '0';
        side.style.transform = 'translateX(20px)';
        setTimeout(() => {
            side.style.transition = 'all 0.6s ease';
            side.style.opacity = '1';
            side.style.transform = 'translateX(0)';
        }, 200 + (index * 100));
    });
});