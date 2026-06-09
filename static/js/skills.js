document.addEventListener('DOMContentLoaded', () => {
    const nodes = document.querySelectorAll('.skill-card');

    const nodeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = parseInt(entry.target.getAttribute('data-delay')) || 0;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, delay);
                nodeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08 });

    nodes.forEach(node => nodeObserver.observe(node));
});
