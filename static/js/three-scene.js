/**
 * Nithin Dharavath - Kinetic 3D Studio Sculpture & Depth Engine
 * Powered by Three.js (r128)
 * 
 * Aesthetic: Dark luxury studio, generative 3D animated kinetic dot cloud / neural field
 * floating behind the name with interactive mouse parallax & damping.
 */

(function () {
    'use strict';

    function isWebGLAvailable() {
        try {
            const canvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
        } catch (e) {
            return false;
        }
    }

    if (!isWebGLAvailable() || typeof THREE === 'undefined') {
        return;
    }

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ==========================================================================
       1. Background Spatial Dot Matrix & Parallax (Deep Obsidian Ambiance)
       ========================================================================== */
    function initBackgroundSpatialGrid() {
        const canvas = document.getElementById('bg-3d-canvas');
        if (!canvas) return;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 1200);
        camera.position.z = 500;

        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
            powerPreference: 'high-performance'
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        const pointCount = window.innerWidth < 768 ? 50 : 100;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(pointCount * 3);
        const velocities = [];

        const bounds = { x: 550, y: 400, z: 250 };

        for (let i = 0; i < pointCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * bounds.x * 2;
            positions[i * 3 + 1] = (Math.random() - 0.5) * bounds.y * 2;
            positions[i * 3 + 2] = (Math.random() - 0.5) * bounds.z * 2;

            velocities.push({
                x: (Math.random() - 0.5) * 0.1,
                y: (Math.random() - 0.5) * 0.1,
                z: (Math.random() - 0.5) * 0.05
            });
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const createDotTexture = () => {
            const size = 32;
            const texCanvas = document.createElement('canvas');
            texCanvas.width = size;
            texCanvas.height = size;
            const ctx = texCanvas.getContext('2d');
            const gradient = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
            gradient.addColorStop(0, 'rgba(255, 255, 255, 0.6)');
            gradient.addColorStop(0.3, 'rgba(240, 68, 56, 0.25)');
            gradient.addColorStop(0.8, 'rgba(240, 68, 56, 0.05)');
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, size, size);
            return new THREE.CanvasTexture(texCanvas);
        };

        const material = new THREE.PointsMaterial({
            size: 4,
            map: createDotTexture(),
            transparent: true,
            opacity: 0.45,
            depthWrite: false
        });

        const points = new THREE.Points(geometry, material);
        scene.add(points);

        let mouseX = 0;
        let mouseY = 0;
        let targetX = 0;
        let targetY = 0;
        let scrollY = 0;

        window.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX - window.innerWidth / 2) * 0.02;
            mouseY = (e.clientY - window.innerHeight / 2) * 0.02;
        }, { passive: true });

        window.addEventListener('scroll', () => {
            scrollY = window.pageYOffset * 0.08;
        }, { passive: true });

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }, { passive: true });

        function animate() {
            requestAnimationFrame(animate);

            targetX += (mouseX - targetX) * 0.04;
            targetY += (mouseY - targetY) * 0.04;

            camera.position.x = targetX;
            camera.position.y = -targetY - scrollY * 0.2;
            camera.lookAt(scene.position);

            const pos = geometry.attributes.position.array;
            for (let i = 0; i < pointCount; i++) {
                pos[i * 3] += velocities[i].x;
                pos[i * 3 + 1] += velocities[i].y;
                pos[i * 3 + 2] += velocities[i].z;

                if (Math.abs(pos[i * 3]) > bounds.x) velocities[i].x *= -1;
                if (Math.abs(pos[i * 3 + 1]) > bounds.y) velocities[i].y *= -1;
                if (Math.abs(pos[i * 3 + 2]) > bounds.z) velocities[i].z *= -1;
            }
            geometry.attributes.position.needsUpdate = true;

            points.rotation.y += 0.0003;

            renderer.render(scene, camera);
        }

        animate();
    }

    /* ==========================================================================
       2. Hero Center Stage 3D Animated Kinetic Dots & Neural Particle Field
          (Replaced solid loop with interactive glowing 3D animated dots)
       ========================================================================== */
    /* ==========================================================================
       2. Hero Center Stage Minimal 3D Neural Constellation (Neutral Theme)
       ========================================================================== */
    function initHeroSculpture() {
        const container = document.querySelector('.hero-center-stage') || 
                          document.querySelector('.hero-3d-container') ||
                          document.querySelector('.focal-media-box');
        const canvas = document.getElementById('hero-3d-canvas');
        if (!container || !canvas) return;

        const width = container.clientWidth || 1100;
        const height = container.clientHeight || 480;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
        camera.position.set(0, 0, 7.5);

        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
            powerPreference: 'high-performance'
        });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        const stageGroup = new THREE.Group();
        scene.add(stageGroup);

        // Minimal, crisp neutral circular dot texture (No additive flare, pure soft slate)
        const createNeutralDotTexture = () => {
            const size = 32;
            const texCanvas = document.createElement('canvas');
            texCanvas.width = size;
            texCanvas.height = size;
            const ctx = texCanvas.getContext('2d');
            const center = size / 2;
            const radius = size * 0.42;

            ctx.clearRect(0, 0, size, size);
            ctx.beginPath();
            ctx.arc(center, center, radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(148, 163, 184, 0.85)';
            ctx.fill();

            return new THREE.CanvasTexture(texCanvas);
        };

        const dotTexture = createNeutralDotTexture();

        // Minimal Neural Node Cloud (Discrete, spacious, elegant)
        const nodeCount = 95;
        const positions = new Float32Array(nodeCount * 3);
        const velocities = [];
        const bounds = { x: 5.2, y: 2.2, z: 2.8 };

        for (let i = 0; i < nodeCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * bounds.x * 2;
            positions[i * 3 + 1] = (Math.random() - 0.5) * bounds.y * 2;
            positions[i * 3 + 2] = (Math.random() - 0.5) * bounds.z * 2;

            velocities.push({
                x: (Math.random() - 0.5) * 0.004,
                y: (Math.random() - 0.5) * 0.004,
                z: (Math.random() - 0.5) * 0.003
            });
        }

        const nodeGeo = new THREE.BufferGeometry();
        nodeGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const nodeMat = new THREE.PointsMaterial({
            size: 3.2,
            map: dotTexture,
            transparent: true,
            opacity: 0.55,
            depthWrite: false
        });

        const nodePoints = new THREE.Points(nodeGeo, nodeMat);
        stageGroup.add(nodePoints);

        // Dynamic Neural Link Lines between nearby nodes
        const maxLines = 160;
        const linePositions = new Float32Array(maxLines * 2 * 3);
        const lineGeo = new THREE.BufferGeometry();
        lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));

        const lineMat = new THREE.LineBasicMaterial({
            color: 0x475569,
            transparent: true,
            opacity: 0.22,
            depthWrite: false
        });

        const lineSegments = new THREE.LineSegments(lineGeo, lineMat);
        stageGroup.add(lineSegments);

        // Interaction state
        let isDragging = false;
        let previousMousePosition = { x: 0, y: 0 };
        let mouseNormalized = { x: 0, y: 0 };
        let targetRotation = { x: 0, y: 0 };

        function onPointerDown(e) {
            isDragging = true;
            previousMousePosition = {
                x: e.clientX || (e.touches && e.touches[0].clientX) || 0,
                y: e.clientY || (e.touches && e.touches[0].clientY) || 0
            };
        }

        function onPointerMove(e) {
            const clientX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
            const clientY = e.clientY || (e.touches && e.touches[0].clientY) || 0;

            const rect = container.getBoundingClientRect();
            mouseNormalized.x = ((clientX - rect.left) / rect.width) * 2 - 1;
            mouseNormalized.y = -(((clientY - rect.top) / rect.height) * 2 - 1);

            targetRotation.y = mouseNormalized.x * 0.35;
            targetRotation.x = -mouseNormalized.y * 0.25;

            if (isDragging) {
                const deltaX = clientX - previousMousePosition.x;
                const deltaY = clientY - previousMousePosition.y;

                stageGroup.rotation.y += deltaX * 0.005;
                stageGroup.rotation.x += deltaY * 0.005;

                previousMousePosition = { x: clientX, y: clientY };
            }
        }

        function onPointerUp() {
            isDragging = false;
        }

        container.addEventListener('mousedown', onPointerDown);
        window.addEventListener('mousemove', onPointerMove, { passive: true });
        window.addEventListener('mouseup', onPointerUp);

        container.addEventListener('touchstart', onPointerDown, { passive: true });
        window.addEventListener('touchmove', onPointerMove, { passive: true });
        window.addEventListener('touchend', onPointerUp, { passive: true });

        const connectionDistance = 2.1;

        function renderSculpture() {
            requestAnimationFrame(renderSculpture);

            // Gentle natural drift and boundary rebound
            const pos = nodeGeo.attributes.position.array;
            for (let i = 0; i < nodeCount; i++) {
                const i3 = i * 3;
                pos[i3] += velocities[i].x;
                pos[i3 + 1] += velocities[i].y;
                pos[i3 + 2] += velocities[i].z;

                if (Math.abs(pos[i3]) > bounds.x) velocities[i].x *= -1;
                if (Math.abs(pos[i3 + 1]) > bounds.y) velocities[i].y *= -1;
                if (Math.abs(pos[i3 + 2]) > bounds.z) velocities[i].z *= -1;
            }
            nodeGeo.attributes.position.needsUpdate = true;

            // Update connecting lines
            let lineIdx = 0;
            const lPos = lineGeo.attributes.position.array;
            for (let i = 0; i < nodeCount && lineIdx < maxLines; i++) {
                const x1 = pos[i * 3];
                const y1 = pos[i * 3 + 1];
                const z1 = pos[i * 3 + 2];

                for (let j = i + 1; j < nodeCount && lineIdx < maxLines; j++) {
                    const x2 = pos[j * 3];
                    const y2 = pos[j * 3 + 1];
                    const z2 = pos[j * 3 + 2];

                    const dx = x1 - x2;
                    const dy = y1 - y2;
                    const dz = z1 - z2;
                    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                    if (dist < connectionDistance) {
                        const ptr = lineIdx * 6;
                        lPos[ptr] = x1;
                        lPos[ptr + 1] = y1;
                        lPos[ptr + 2] = z1;
                        lPos[ptr + 3] = x2;
                        lPos[ptr + 4] = y2;
                        lPos[ptr + 5] = z2;
                        lineIdx++;
                    }
                }
            }

            // Zero out remaining line positions
            for (let k = lineIdx * 6; k < maxLines * 6; k++) {
                lPos[k] = 0;
            }
            lineGeo.attributes.position.needsUpdate = true;

            // Smooth parallax rotation towards target
            if (!isDragging) {
                stageGroup.rotation.y += (targetRotation.y - stageGroup.rotation.y) * 0.05 + 0.0006;
                stageGroup.rotation.x += (targetRotation.x - stageGroup.rotation.x) * 0.05;
            }

            renderer.render(scene, camera);
        }

        renderSculpture();

        window.addEventListener('resize', () => {
            const w = container.clientWidth || 1100;
            const h = container.clientHeight || 480;
            if (w > 0 && h > 0) {
                camera.aspect = w / h;
                camera.updateProjectionMatrix();
                renderer.setSize(w, h);
            }
        }, { passive: true });
    }

    /* ==========================================================================
       3. Subtle 3D Card Hover Perspective
       ========================================================================== */
    function initCard3DTilt() {
        if (prefersReducedMotion) return;

        const tiltCards = document.querySelectorAll('.service-card, .project-card, .stat-card, .detail-item');

        tiltCards.forEach((card) => {
            let isInside = false;

            card.addEventListener('pointerenter', () => {
                isInside = true;
            });

            card.addEventListener('pointermove', (e) => {
                if (!isInside) return;

                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((y - centerY) / centerY) * -3;
                const rotateY = ((x - centerX) / centerX) * 3;

                card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-3px)`;
            });

            card.addEventListener('pointerleave', () => {
                isInside = false;
                card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initBackgroundSpatialGrid();
            initHeroSculpture();
            initCard3DTilt();
        });
    } else {
        initBackgroundSpatialGrid();
        initHeroSculpture();
        initCard3DTilt();
    }
})();
