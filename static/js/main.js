document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // Mobile Navigation Toggle
    // -------------------------------------------------------------
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            const isOpen = navLinks.classList.toggle('active');
            navToggle.classList.toggle('open', isOpen);
            navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            if (isOpen) {
                document.body.classList.add('nav-menu-open');
            } else {
                document.body.classList.remove('nav-menu-open');
            }
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                navToggle.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('nav-menu-open');
            });
        });

        // Close mobile menu on Escape key
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                navToggle.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('nav-menu-open');
                navToggle.focus();
            }
        });

        // Close mobile menu on resize to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                navToggle.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('nav-menu-open');
            }
        });
    }

    // -------------------------------------------------------------
    // Active Navigation Highlighting & Scroll Progress Tracker
    // -------------------------------------------------------------
    const sections = document.querySelectorAll('section');
    const navLinksArray = document.querySelectorAll('.nav-link');
    const dockButtons = document.querySelectorAll('.dock-btn');
    const scrollTrackerThumb = document.querySelector('.scroll-tracker-thumb');

    const updateScrollState = () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.pageYOffset >= (sectionTop - 150)) {
                current = section.getAttribute('id') || '';
            }
        });

        navLinksArray.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href') || '';
            if (current && href.includes(current)) {
                link.classList.add('active');
            } else if (!current && href === '/') {
                link.classList.add('active');
            }
        });

        dockButtons.forEach(btn => {
            btn.classList.remove('active');
            const href = btn.getAttribute('href') || '';
            if (current && href.includes(current)) {
                btn.classList.add('active');
            } else if (!current && href === '/') {
                btn.classList.add('active');
            }
        });

        if (scrollTrackerThumb) {
            const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
            if (maxScroll > 0) {
                const scrollPercent = Math.min(Math.max(window.pageYOffset / maxScroll, 0), 1);
                scrollTrackerThumb.style.top = `${scrollPercent * 100}%`;
            }
        }
    };

    window.addEventListener('scroll', updateScrollState, { passive: true });
    updateScrollState();

    // -------------------------------------------------------------
    // Real-Time Clock (Matching "New York 10:12 AM" in reference image)
    // -------------------------------------------------------------
    const liveTimeElements = [
        document.getElementById('clock-live-time'),
        document.getElementById('clock-time')
    ];

    const updateLiveTime = () => {
        const now = new Date();
        const options = {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
            timeZone: 'Asia/Kolkata'
        };
        try {
            const timeString = new Intl.DateTimeFormat('en-US', options).format(now);
            liveTimeElements.forEach(el => {
                if (el) el.textContent = timeString;
            });
        } catch {
            const hours = now.getHours();
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            const formattedHours = hours % 12 || 12;
            const fallback = `${formattedHours}:${minutes} ${ampm}`;
            liveTimeElements.forEach(el => {
                if (el) el.textContent = fallback;
            });
        }
    };

    updateLiveTime();
    setInterval(updateLiveTime, 1000);

    // -------------------------------------------------------------
    // Skill Section Bars Animation
    // -------------------------------------------------------------
    const skillBars = document.querySelectorAll('.skill-progress');
    // -------------------------------------------------------------
    // Interactive Curiosity Tab Switching Logic
    // -------------------------------------------------------------
    const curiosityTabs = document.querySelectorAll('.curiosity-tab-btn');
    const curiosityPanels = document.querySelectorAll('.curiosity-panel');

    if (curiosityTabs.length > 0 && curiosityPanels.length > 0) {
        curiosityTabs.forEach((tab) => {
            tab.addEventListener('click', () => {
                const targetTabId = tab.dataset.tab;
                if (!targetTabId) return;

                // Update tab buttons
                curiosityTabs.forEach((t) => {
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                });
                tab.classList.add('active');
                tab.setAttribute('aria-selected', 'true');

                // Switch panels
                curiosityPanels.forEach((panel) => {
                    if (panel.id === `curiosity-panel-${targetTabId}`) {
                        panel.classList.add('active');
                    } else {
                        panel.classList.remove('active');
                    }
                });
            });

            // Keyboard accessibility for tablist (ArrowLeft, ArrowRight)
            tab.addEventListener('keydown', (e) => {
                const tabsArray = Array.from(curiosityTabs);
                const currentIndex = tabsArray.indexOf(tab);
                let newIndex = null;

                if (e.key === 'ArrowRight') {
                    newIndex = (currentIndex + 1) % tabsArray.length;
                } else if (e.key === 'ArrowLeft') {
                    newIndex = (currentIndex - 1 + tabsArray.length) % tabsArray.length;
                }

                if (newIndex !== null) {
                    e.preventDefault();
                    tabsArray[newIndex].focus();
                    tabsArray[newIndex].click();
                }
            });
        });
    }

    // -------------------------------------------------------------
    // Contact Form AJAX Submission with Status Feedback
    // -------------------------------------------------------------
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
