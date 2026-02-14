const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');
const menuIcon = document.getElementById('menuIcon');

menuToggle.addEventListener('click', () => {
    // Toggle menu
    mobileMenu.classList.toggle('active');
    
    // Toggle icon between bars and times
    if (mobileMenu.classList.contains('active')) {
        menuIcon.classList.remove('fa-bars');
        menuIcon.classList.add('fa-times');
        document.body.classList.add('menu-open');
    } else {
        menuIcon.classList.remove('fa-times');
        menuIcon.classList.add('fa-bars');
        document.body.classList.remove('menu-open');
    }
});

// Close menu when clicking on a link
document.querySelectorAll('.mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        menuIcon.classList.remove('fa-times');
        menuIcon.classList.add('fa-bars');
        document.body.classList.remove('menu-open');
    });
});

// Close menu on window resize if going to desktop
window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) { // md breakpoint
        mobileMenu.classList.remove('active');
        menuIcon.classList.remove('fa-times');
        menuIcon.classList.add('fa-bars');
        document.body.classList.remove('menu-open');
    }
});