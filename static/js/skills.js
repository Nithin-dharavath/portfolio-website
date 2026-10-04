document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // Dynamic Category Filtering for Bento Cards
    // -------------------------------------------------------------
    const filterButtons = document.querySelectorAll('.filter-btn');
    const bentoCards = document.querySelectorAll('.bento-card');

    const animateMeters = (container = document) => {
        const meters = container.querySelectorAll('.meter-fill');
        meters.forEach(meter => {
            const targetWidth = meter.style.width;
            meter.style.width = '0%';
            setTimeout(() => {
                meter.style.transition = 'width 0.9s cubic-bezier(0.16, 1, 0.3, 1)';
                meter.style.width = targetWidth;
            }, 60);
        });
    };

    // Initial animation for bento card meters
    setTimeout(() => {
        animateMeters();
    }, 150);

    // -------------------------------------------------------------
    // Animate Dashboard Bar Chart and Horizontal Meters on Load
    // -------------------------------------------------------------
    const animateDashboard = () => {
        const barFills = document.querySelectorAll('.dash-barchart-block .bar-fill');
        barFills.forEach((bar, i) => {
            const targetHeight = bar.getAttribute('data-height') || bar.style.height || '90%';
            bar.style.height = '0%';
            setTimeout(() => {
                bar.style.transition = 'height 1s cubic-bezier(0.16, 1, 0.3, 1)';
                bar.style.height = targetHeight;
            }, 60 + i * 40);
        });

        const dashMeters = document.querySelectorAll('.dash-meter-fill');
        dashMeters.forEach((meter, i) => {
            const targetWidth = meter.style.width || '90%';
            meter.style.width = '0%';
            setTimeout(() => {
                meter.style.transition = 'width 1s cubic-bezier(0.16, 1, 0.3, 1)';
                meter.style.width = targetWidth;
            }, 80 + i * 50);
        });
    };

    setTimeout(animateDashboard, 100);

    if (filterButtons.length > 0 && bentoCards.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.getAttribute('data-category');

                // Update active button state
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Filter cards: show only the single selected category card
                bentoCards.forEach(card => {
                    const cardCat = card.getAttribute('data-category');
                    if (cardCat === category) {
                        card.classList.remove('is-hidden');
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(12px)';
                        setTimeout(() => {
                            card.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                            animateMeters(card);
                        }, 20);
                    } else {
                        card.classList.add('is-hidden');
                    }
                });
            });
        });
    }

    // -------------------------------------------------------------
    // 3D Perspective Card Tilt on Mouse Hover
    // -------------------------------------------------------------
    bentoCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -3;
            const rotateY = ((x - centerX) / centerX) * 3;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
            card.style.transition = 'transform 0.4s ease';
        });

        card.addEventListener('mouseenter', () => {
            card.style.transition = 'none';
        });
    });
});
