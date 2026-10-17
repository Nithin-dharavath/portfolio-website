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

        // Light Hero Navigation & Floating Dock Visibility
        const mainNav = document.querySelector('.main-nav');
        const heroSection = document.getElementById('home');
        const heroHeight = heroSection ? (heroSection.offsetHeight - 120) : 400;

        if (window.pageYOffset > 50) {
            if (mainNav) mainNav.classList.add('nav-scrolled');
        } else {
            if (mainNav) mainNav.classList.remove('nav-scrolled');
        }

        if (window.pageYOffset > heroHeight) {
            document.body.classList.add('scrolled-past-hero');
        } else {
            document.body.classList.remove('scrolled-past-hero');
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
    // Contact Form AJAX Handler with Accessible Feedback
    // -------------------------------------------------------------
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        const feedbackEl = document.getElementById('contact-form-feedback');
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button[type="submit"]') || contactForm.querySelector('button');
            const originalHtml = btn.innerHTML;

            if (feedbackEl) {
                feedbackEl.className = 'form-feedback';
                feedbackEl.textContent = '';
            }

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
                    btn.className = 'btn btn-primary btn-submit full-width btn-success';
                    if (feedbackEl) {
                        feedbackEl.className = 'form-feedback is-visible success';
                        feedbackEl.textContent = data.message || 'Thank you! Your message has been sent successfully.';
                    }
                    contactForm.reset();
                    setTimeout(() => {
                        btn.innerHTML = originalHtml;
                        btn.disabled = false;
                        btn.className = 'btn btn-primary btn-submit full-width';
                    }, 4000);
                } else {
                    btn.innerText = 'Failed to Send';
                    btn.className = 'btn btn-primary btn-submit full-width btn-error';
                    if (feedbackEl) {
                        feedbackEl.className = 'form-feedback is-visible error';
                        if (data.errors && Array.isArray(data.errors)) {
                            feedbackEl.textContent = data.errors.join(' ');
                        } else {
                            feedbackEl.textContent = data.message || 'Unable to send message. Please review the form fields.';
                        }
                    }
                    setTimeout(() => {
                        btn.innerHTML = originalHtml;
                        btn.disabled = false;
                        btn.className = 'btn btn-primary btn-submit full-width';
                    }, 3500);
                }
            } catch {
                clearTimeout(timeoutId);
                btn.innerText = 'Connection Error';
                btn.className = 'btn btn-primary btn-submit full-width btn-error';
                if (feedbackEl) {
                    feedbackEl.className = 'form-feedback is-visible error';
                    feedbackEl.textContent = 'Network or server timeout. Please check your connection and try again.';
                }
                setTimeout(() => {
                    btn.innerHTML = originalHtml;
                    btn.disabled = false;
                    btn.className = 'btn btn-primary btn-submit full-width';
                }, 3500);
            }
        });
    }

    // -------------------------------------------------------------
    // Hero Floating Card Carousel (Real Projects Highlight)
    // -------------------------------------------------------------
    const cardTag = document.getElementById('card-tag');
    const cardTitle = document.getElementById('card-title');
    const cardSub = document.getElementById('card-sub');
    const cardProgress = document.getElementById('card-progress');
    const btnPrev = document.getElementById('card-btn-prev');
    const btnNext = document.getElementById('card-btn-next');

    if (cardTitle && cardSub && btnPrev && btnNext) {
        const highlights = [
            {
                tag: 'SYSTEM HIGHLIGHT',
                title: 'Code to create.',
                sub: 'Ideas into systems.',
                progress: '60%'
            },
            {
                tag: 'AI AGENTS',
                title: 'Autonomous Swarms',
                sub: 'Stateful tool-calling networks.',
                progress: '85%'
            },
            {
                tag: 'BACKEND ARCHITECTURE',
                title: 'High-Throughput APIs',
                sub: 'FastAPI & async databases.',
                progress: '100%'
            }
        ];

        let currentIndex = 0;

        const updateHighlightCard = (index) => {
            const item = highlights[index];
            if (!item) return;

            cardTitle.style.transition = 'opacity 0.15s ease';
            cardSub.style.transition = 'opacity 0.15s ease';
            cardTitle.style.opacity = '0';
            cardSub.style.opacity = '0';

            setTimeout(() => {
                if (cardTag) cardTag.textContent = item.tag;
                cardTitle.textContent = item.title;
                cardSub.textContent = item.sub;
                if (cardProgress) cardProgress.style.width = item.progress;

                cardTitle.style.opacity = '1';
                cardSub.style.opacity = '1';
            }, 150);
        };

        btnPrev.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + highlights.length) % highlights.length;
            updateHighlightCard(currentIndex);
        });

        btnNext.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % highlights.length;
            updateHighlightCard(currentIndex);
        });
    }

    // -------------------------------------------------------------
    // Hero Video Playback & Fallback Handling
    // -------------------------------------------------------------
    const heroVideo = document.querySelector('.hero-cyber-video');
    const heroFallback = document.querySelector('.hero-video-fallback');

    if (heroVideo) {
        heroVideo.muted = true;

        heroVideo.addEventListener('error', () => {
            if (heroFallback) {
                heroFallback.style.display = 'block';
                heroVideo.style.display = 'none';
            }
        });

        const tryPlay = () => {
            const playPromise = heroVideo.play();
            if (playPromise !== undefined) {
                playPromise.catch(() => {
                    // Autoplay paused by browser policy; poster image remains visible
                });
            }
        };

        if (heroVideo.readyState >= 2) {
            tryPlay();
        } else {
            heroVideo.addEventListener('canplay', tryPlay, { once: true });
        }
    }

    // -------------------------------------------------------------
    // Featured Projects Category Filtering & Carousel Navigation
    // -------------------------------------------------------------
    const projectFilterChips = document.querySelectorAll('.project-filter-chip');
    const projectCards = document.querySelectorAll('.editorial-card');
    const projectsEmptyState = document.getElementById('projects-empty-state');
    const carouselDots = document.querySelectorAll('.carousel-dot-btn');
    const btnProjectPrev = document.getElementById('projects-btn-prev');
    const btnProjectNext = document.getElementById('projects-btn-next');
    const projectsTrack = document.getElementById('projects-track');

    if (projectFilterChips.length > 0 && projectCards.length > 0) {
        projectFilterChips.forEach((chip) => {
            chip.addEventListener('click', () => {
                const filter = chip.dataset.filter || 'all';

                projectFilterChips.forEach((c) => {
                    c.classList.remove('active');
                    c.setAttribute('aria-selected', 'false');
                });
                chip.classList.add('active');
                chip.setAttribute('aria-selected', 'true');

                let visibleCount = 0;
                projectCards.forEach((card) => {
                    const categories = (card.dataset.category || '').split(' ');
                    if (filter === 'all' || categories.includes(filter)) {
                        card.style.display = 'flex';
                        card.style.opacity = '1';
                        visibleCount++;
                    } else {
                        card.style.opacity = '0';
                        card.style.display = 'none';
                    }
                });

                if (projectsEmptyState) {
                    if (visibleCount === 0) {
                        projectsEmptyState.hidden = false;
                    } else {
                        projectsEmptyState.hidden = true;
                    }
                }
            });
        });
    }

    if (carouselDots.length > 0 && projectCards.length > 0) {
        let activeCardIndex = 0;

        const setActiveCard = (index) => {
            const boundedIndex = (index + projectCards.length) % projectCards.length;
            activeCardIndex = boundedIndex;

            carouselDots.forEach((dot, idx) => {
                dot.classList.toggle('active', idx === boundedIndex);
            });

            const targetCard = projectCards[boundedIndex];
            if (targetCard && window.innerWidth <= 1024) {
                targetCard.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            }
        };

        carouselDots.forEach((dot) => {
            dot.addEventListener('click', () => {
                const index = parseInt(dot.dataset.index || '0', 10);
                setActiveCard(index);
            });
        });

        if (btnProjectPrev) {
            btnProjectPrev.addEventListener('click', () => {
                setActiveCard(activeCardIndex - 1);
            });
        }

        if (btnProjectNext) {
            btnProjectNext.addEventListener('click', () => {
                setActiveCard(activeCardIndex + 1);
            });
        }
    }
});

