class AnimationController {
    constructor() {
        this.animations = [];
        this.running = false;
    }

    start() {
        if (!this.running) {
            this.running = true;
            this.animate();
        }
    }

    stop() {
        this.running = false;
    }

    animate() {
        if (!this.running) return;

        const now = Date.now();
        
        this.animations = this.animations.filter(anim => {
            const elapsed = now - anim.startTime;
            const progress = Math.min(elapsed / anim.duration, 1);
            
            anim.update(progress);
            
            if (progress >= 1) {
                if (anim.onComplete) anim.onComplete();
                return false;
            }
            
            return true;
        });

        requestAnimationFrame(() => this.animate());
    }

    addAnimation(config) {
        const animation = {
            startTime: Date.now(),
            duration: config.duration || 1000,
            update: config.update,
            onComplete: config.onComplete
        };

        this.animations.push(animation);
        this.start();
    }

    moveToken(element, fromX, fromY, toX, toY, duration = 500) {
        this.addAnimation({
            duration: duration,
            update: (progress) => {
                const eased = this.easeInOutCubic(progress);
                const currentX = fromX + (toX - fromX) * eased;
                const currentY = fromY + (toY - fromY) * eased;
                
                element.style.left = currentX + 'px';
                element.style.top = currentY + 'px';
            }
        });
    }

    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';
        
        this.addAnimation({
            duration: duration,
            update: (progress) => {
                element.style.opacity = progress.toString();
            }
        });
    }

    fadeOut(element, duration = 300) {
        this.addAnimation({
            duration: duration,
            update: (progress) => {
                element.style.opacity = (1 - progress).toString();
            },
            onComplete: () => {
                element.style.display = 'none';
            }
        });
    }

    pulse(element, duration = 600) {
        const originalScale = element.style.transform || 'scale(1)';
        
        this.addAnimation({
            duration: duration,
            update: (progress) => {
                const scale = 1 + Math.sin(progress * Math.PI) * 0.2;
                element.style.transform = `scale(${scale})`;
            },
            onComplete: () => {
                element.style.transform = originalScale;
            }
        });
    }

    easeInOutCubic(t) {
        return t < 0.5
            ? 4 * t * t * t
            : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
}

const animationController = new AnimationController();