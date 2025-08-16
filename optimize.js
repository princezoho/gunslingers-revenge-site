// Performance optimizations for Gunslinger's Revenge website

// Lazy loading for images
document.addEventListener('DOMContentLoaded', function() {
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Preload critical resources
    const preloadLink = document.createElement('link');
    preloadLink.rel = 'preload';
    preloadLink.as = 'font';
    preloadLink.href = 'assets/wanted.ttf';
    preloadLink.type = 'font/ttf';
    preloadLink.crossOrigin = 'anonymous';
    document.head.appendChild(preloadLink);
    
    // Defer non-critical CSS
    const deferCSS = function() {
        const links = document.querySelectorAll('link[data-defer]');
        links.forEach(link => {
            link.removeAttribute('data-defer');
            link.media = 'all';
        });
    };
    
    if (window.requestIdleCallback) {
        requestIdleCallback(deferCSS);
    } else {
        setTimeout(deferCSS, 100);
    }
    
    // Progressive enhancement for newsletter form
    const newsletterForms = document.querySelectorAll('.newsletter-form, .newsletter-form-popup');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = form.querySelector('input[type="email"]').value;
            
            // Track conversion
            if (typeof gtag !== 'undefined') {
                gtag('event', 'newsletter_signup', {
                    'event_category': 'engagement',
                    'event_label': 'newsletter'
                });
            }
            
            // Redirect to subscribe page with email
            window.open('https://subscribepage.io/U500SL?email=' + encodeURIComponent(email), '_blank');
        });
    });
    
    // Optimize GIF loading - pause when not visible
    const gifs = document.querySelectorAll('.character-bg-section, .full-bg-section');
    
    const gifObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
            } else {
                entry.target.style.animationPlayState = 'paused';
            }
        });
    });
    
    gifs.forEach(gif => gifObserver.observe(gif));
    
    // Service Worker for offline support and caching
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(function(error) {
            console.log('Service Worker registration failed:', error);
        });
    }
});

// Optimize scroll performance
let ticking = false;
function requestTick() {
    if (!ticking) {
        window.requestAnimationFrame(updateElements);
        ticking = true;
    }
}

function updateElements() {
    ticking = false;
    // Update parallax or other scroll-based effects here
}

window.addEventListener('scroll', requestTick, { passive: true });

// Prefetch links on hover
document.addEventListener('mouseover', function(e) {
    if (e.target.tagName === 'A' && e.target.href && e.target.hostname === location.hostname) {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = e.target.href;
        document.head.appendChild(link);
    }
});