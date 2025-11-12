import { useEffect, useRef } from 'react';

/**
 * Organic Blob Background Animation
 * Inspired by landonorris.com - floating morphing blobs
 */
export function OrganicBlobs() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Blob class
    class Blob {
      x: number;
      y: number;
      radius: number;
      vx: number;
      vy: number;
      color: string;
      morphSpeed: number;
      morphOffset: number;

      constructor(canvasWidth: number, canvasHeight: number) {
        this.x = Math.random() * canvasWidth;
        this.y = Math.random() * canvasHeight;
        this.radius = Math.random() * 150 + 100;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.color = `rgba(210, 255, 0, ${Math.random() * 0.08 + 0.02})`;
        this.morphSpeed = Math.random() * 0.02 + 0.01;
        this.morphOffset = Math.random() * Math.PI * 2;
      }

      update(time: number, canvasWidth: number, canvasHeight: number) {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off edges
        if (this.x < -this.radius || this.x > canvasWidth + this.radius) {
          this.vx *= -1;
        }
        if (this.y < -this.radius || this.y > canvasHeight + this.radius) {
          this.vy *= -1;
        }
      }

      draw(ctx: CanvasRenderingContext2D, time: number) {
        const points = 8;
        const angleStep = (Math.PI * 2) / points;
        
        ctx.beginPath();
        
        for (let i = 0; i <= points; i++) {
          const angle = i * angleStep;
          const morphValue = Math.sin(time * this.morphSpeed + this.morphOffset + angle * 2) * 20;
          const radius = this.radius + morphValue;
          const x = this.x + Math.cos(angle) * radius;
          const y = this.y + Math.sin(angle) * radius;
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        
        ctx.closePath();
        ctx.fillStyle = this.color;
        ctx.fill();
      }
    }

    // Create blobs
    const blobs: Blob[] = [];
    const blobCount = window.innerWidth < 768 ? 3 : 6;
    
    for (let i = 0; i < blobCount; i++) {
      blobs.push(new Blob(canvas.width, canvas.height));
    }

    // Animation loop
    let animationId: number;
    let startTime = Date.now();

    const animate = () => {
      const currentTime = (Date.now() - startTime) / 1000;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      blobs.forEach(blob => {
        blob.update(currentTime, canvas.width, canvas.height);
        blob.draw(ctx, currentTime);
      });
      
      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ opacity: 0.6 }}
    />
  );
}
