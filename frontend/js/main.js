document.addEventListener('DOMContentLoaded', () => {

    // 1. Boot Sequence
    const bootScreen = document.getElementById('boot-screen');
    const bootDecrypt = document.getElementById('boot-decrypt');
    
    if (bootScreen) {
        let decCount = 0;
        const decInterval = setInterval(() => {
            bootDecrypt.textContent += '.';
            decCount++;
            if (decCount > 3) {
                clearInterval(decInterval);
                bootScreen.style.opacity = '0';
                setTimeout(() => {
                    bootScreen.style.display = 'none';
                    initCanvas();
                }, 500);
            }
        }, 500);
    }

    // 2. Text Scramble Hover Effect for Nav
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*';
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            const originalText = link.dataset.text;
            let iterations = 0;
            
            clearInterval(link.scrambleInterval);
            
            link.scrambleInterval = setInterval(() => {
                link.innerText = originalText.split('').map((char, index) => {
                    if (index < iterations) {
                        return originalText[index];
                    }
                    return chars[Math.floor(Math.random() * chars.length)];
                }).join('');
                
                if (iterations >= originalText.length) {
                    clearInterval(link.scrambleInterval);
                }
                
                iterations += 1 / 3;
            }, 30);
        });
    });

    // 3. Live UTC Clock
    const clockEl = document.getElementById('live-clock');
    if (clockEl) {
        setInterval(() => {
            const now = new Date();
            const timeString = now.toISOString().split('T')[1].split('.')[0];
            clockEl.textContent = `UTC: ${timeString}`;
        }, 1000);
    }

    // 4. Threat Counter Animation
    const counterEl = document.getElementById('counter');
    if (counterEl) {
        let count = 1000;
        const target = 1247;
        
        const updateCounter = () => {
            if (count < target) {
                count += Math.floor(Math.random() * 5) + 1;
                if (count > target) count = target;
                counterEl.textContent = count.toLocaleString();
                setTimeout(updateCounter, 30);
            } else {
                // Occasionally bump the number
                setInterval(() => {
                    if (Math.random() > 0.7) {
                        count += Math.floor(Math.random() * 3);
                        counterEl.textContent = count.toLocaleString();
                    }
                }, 2000);
            }
        };
        setTimeout(updateCounter, 2000); // Start after boot
    }

    // 5. Terminal Log Auto-scroll
    const termLog = document.getElementById('term-log');
    if (termLog) {
        const logs = [
            "[INFO] Connection established from 192.168.1.55",
            "[OK] Handshake verified.",
            "[WARN] Failed login attempt for user 'admin'",
            "[INFO] Syncing blockchain ledger... block #489211",
            "[CRITICAL] Perimeter breach attempt on Port 22. IP blocked.",
            "[OK] AI Engine initialized. Model accuracy: 98.4%",
            "[INFO] Routing traffic through secure tunnel.",
            "[WARN] CPU usage spike detected in Node Alpha."
        ];
        
        let logIndex = 0;
        
        const addLog = () => {
            const line = document.createElement('div');
            line.className = 'log-line';
            
            const now = new Date();
            const time = now.toISOString().split('T')[1].split('.')[0];
            
            const logText = logs[logIndex % logs.length];
            let color = 'var(--accent-cyan)';
            if (logText.includes('[WARN]')) color = 'var(--accent-magenta)';
            if (logText.includes('[CRITICAL]')) color = 'var(--accent-magenta)';
            if (logText.includes('[OK]')) color = 'var(--accent-green)';
            
            line.innerHTML = `<span class="log-timestamp">[${time}]</span> <span style="color:${color}">${logText}</span>`;
            termLog.appendChild(line);
            
            // Auto scroll to bottom
            termLog.scrollTop = termLog.scrollHeight;
            
            // Keep max 20 lines
            if (termLog.children.length > 20) {
                termLog.removeChild(termLog.firstChild);
            }
            
            logIndex++;
            setTimeout(addLog, Math.random() * 2000 + 500);
        };
        
        setTimeout(addLog, 2500);
    }

    // 6. Generative Canvas (Particle Network)
    function initCanvas() {
        const canvas = document.getElementById('particle-canvas');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];
        
        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        
        window.addEventListener('resize', resize);
        resize();
        
        class Particle {
            constructor() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.radius = Math.random() * 1.5;
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;
                
                if (this.x < 0 || this.x > width) this.vx *= -1;
                if (this.y < 0 || this.y > height) this.vy *= -1;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(0, 240, 255, 0.5)';
                ctx.fill();
            }
        }
        
        for (let i = 0; i < 50; i++) {
            particles.push(new Particle());
        }
        
        function animate() {
            ctx.clearRect(0, 0, width, height);
            
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            
            // Draw connections
            ctx.beginPath();
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    if (dist < 150) {
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                    }
                }
            }
            ctx.strokeStyle = 'rgba(0, 240, 255, 0.05)';
            ctx.stroke();
            
            requestAnimationFrame(animate);
        }
        
        animate();
    }
});
