document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar'); // base.html-dəki navbar
    
    // Navbar Blur Effekt
    window.addEventListener('scroll', () => {
        if (window.scrollY > 30) {
            navbar.classList.add('navbar-scrolled');
            navbar.style.background = "rgba(11, 15, 25, 0.85)";
            navbar.style.backdropFilter = "blur(15px)";
            navbar.style.padding = "15px 0";
        } else {
            navbar.classList.remove('navbar-scrolled');
            navbar.style.background = "transparent";
            navbar.style.backdropFilter = "none";
            navbar.style.padding = "25px 0";
        }
    });
});


