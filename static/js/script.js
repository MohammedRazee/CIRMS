window.addEventListener('scroll', function() {
    var footer = document.querySelector('footer');
    var bg = document.querySelector('.footer-parallax-bg');
    if (!footer || !bg) return;
    var rect = footer.getBoundingClientRect();
    var windowHeight = window.innerHeight;
    if (rect.top < windowHeight && rect.bottom > 0) {
        var percent = (windowHeight - rect.top) / (rect.height + windowHeight);
        bg.style.transform = 'translateY(' + (percent * 40) + 'px) scale(1.1)';
    }
});