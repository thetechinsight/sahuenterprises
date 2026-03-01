// ===== Sahu Enterprises - Main JS =====

document.addEventListener('DOMContentLoaded', () => {

    // ===== Mobile Navigation Toggle =====
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navToggle.classList.toggle('open');
    });

    // Close mobile nav on link click
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            navToggle.classList.remove('open');
        });
    });

    // ===== Navbar Scroll Effect =====
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ===== Product Tabs =====
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.product-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.tab;

            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(`tab-${target}`).classList.add('active');
        });
    });

    // ===== Language Toggle (EN / HI) =====
    const langBtns = document.querySelectorAll('.lang-btn');
    let currentLang = 'en';

    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            if (lang === currentLang) return;

            currentLang = lang;

            // Update active button
            langBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update all translatable elements
            document.querySelectorAll(`[data-${lang}]`).forEach(el => {
                const text = el.getAttribute(`data-${lang}`);
                if (text) {
                    // Check if the element has child elements with translations
                    if (el.innerHTML.includes('<') && !el.querySelector(`[data-${lang}]`)) {
                        // Element has HTML content (like <br> tags)
                        el.innerHTML = text;
                    } else if (!el.querySelector(`[data-${lang}]`)) {
                        el.textContent = text;
                    }
                }
            });

            // Update HTML lang attribute
            document.documentElement.lang = lang === 'hi' ? 'hi' : 'en';
        });
    });

    // ===== Scroll Animations =====
    const animateElements = () => {
        const cards = document.querySelectorAll(
            '.about-card, .brand-card, .product-card, .advantage-card, .contact-item'
        );

        cards.forEach(card => {
            if (!card.classList.contains('animate-on-scroll')) {
                card.classList.add('animate-on-scroll');
            }
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -40px 0px'
        });

        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    };

    animateElements();

    // ===== Active Nav Link on Scroll =====
    const sections = document.querySelectorAll('section[id]');

    const highlightNav = () => {
        const scrollY = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
                navLinks.querySelectorAll('a').forEach(link => {
                    link.classList.remove('active-link');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active-link');
                    }
                });
            }
        });
    };

    window.addEventListener('scroll', highlightNav);

    // ===== Smooth Scroll for anchor links =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

});
