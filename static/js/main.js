document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navToggle.classList.toggle('open');
        });
    }

    // Smooth Scrolling with Active State Update
    const sections = document.querySelectorAll('section');
    const navLinksArray = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 100)) {
                current = section.getAttribute('id');
            }
        });

        navLinksArray.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });
    });

    // Intersection Observer for Skill Bars Animation
    const skillBars = document.querySelectorAll('.skill-progress');
    const skillSection = document.querySelector('.skill-section');

    if (skillSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    skillBars.forEach(bar => {
                        const targetWidth = bar.style.width;
                        bar.style.transition = 'width 1.5s ease-out';
                        // The width is already set in HTML, but this ensures it animates on entry
                        bar.style.width = targetWidth;
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        observer.observe(skillSection);
    }

    // Form Submission Handling
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'Sending...';
            btn.disabled = true;

            // Simulate API call
            setTimeout(() => {
                btn.innerText = 'Message Sent! ✓';
                btn.style.background = '#22c55e';

                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.disabled = false;
                    btn.style.background = '';
                    contactForm.reset();
                }, 3000);
            }, 1500);
        });
    }
});
