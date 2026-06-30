document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navToggle.classList.toggle('open');
        });
    }

    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                navToggle.classList.remove('open');
            });
        });
    }

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

    const skillBars = document.querySelectorAll('.skill-progress');
    const skillSection = document.querySelector('.skill-section');

    if (skillSection) {
        // Bars start at 0 width via CSS; animate to target on scroll.
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    skillBars.forEach(bar => {
                        bar.style.width = bar.dataset.target + '%';
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        observer.observe(skillSection);
    }

    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'Sending...';
            btn.disabled = true;

            const formData = new FormData(contactForm);
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);

            try {
                const res = await fetch('/api/contact', {
                    method: 'POST',
                    body: formData,
                    signal: controller.signal,
                });
                clearTimeout(timeoutId);
                const data = await res.json();

                if (data.ok) {
                    btn.innerText = 'Message Sent! ✓';
                    btn.className = 'btn btn-success full-width';
                } else {
                    btn.innerText = 'Failed! Try Again';
                    btn.className = 'btn btn-error full-width';
                }
            } catch {
                btn.innerText = 'Failed! Try Again';
                btn.className = 'btn btn-error full-width';
            }

            setTimeout(() => {
                btn.innerText = originalText;
                btn.disabled = false;
                btn.className = 'btn btn-primary full-width';
                contactForm.reset();
            }, 3000);
        });
    }
});
