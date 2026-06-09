document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navToggle.classList.toggle('open');
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
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    skillBars.forEach(bar => {
                        const targetWidth = bar.style.width;
                        bar.style.transition = 'width 1.5s ease-out';
                        bar.style.width = targetWidth;
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

            try {
                const res = await fetch('/api/contact', {
                    method: 'POST',
                    body: formData,
                });
                const data = await res.json();

                if (data.ok) {
                    btn.innerText = 'Message Sent! ✓';
                    btn.style.background = '#22c55e';
                } else {
                    btn.innerText = 'Failed! Try Again';
                    btn.style.background = '#ef4444';
                }
            } catch {
                btn.innerText = 'Failed! Try Again';
                btn.style.background = '#ef4444';
            }

            setTimeout(() => {
                btn.innerText = originalText;
                btn.disabled = false;
                btn.style.background = '';
                contactForm.reset();
            }, 3000);
        });
    }
});
