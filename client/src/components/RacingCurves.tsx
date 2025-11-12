/**
 * Racing Track Curves Background
 * Inspired by landonorris.com - organic S-curves with parallax effect
 */
export function RacingCurves() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden opacity-30">
      <svg
        className="absolute w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
        style={{ transform: 'translateY(var(--scroll-offset, 0px))' }}
      >
        {/* Curve 1 - Top left */}
        <path
          d="M -100 200 Q 300 100, 600 300 T 1200 400"
          stroke="oklch(0.95 0.25 110)"
          strokeWidth="2"
          fill="none"
          opacity="0.15"
        />
        
        {/* Curve 2 - Middle */}
        <path
          d="M 0 500 Q 400 400, 800 600 T 1600 700"
          stroke="oklch(0.75 0.15 210)"
          strokeWidth="1.5"
          fill="none"
          opacity="0.1"
        />
        
        {/* Curve 3 - Bottom right */}
        <path
          d="M 400 800 Q 800 700, 1200 900 T 2000 1000"
          stroke="oklch(0.95 0.25 110)"
          strokeWidth="2"
          fill="none"
          opacity="0.12"
        />
        
        {/* Circular arc - top right */}
        <circle
          cx="80%"
          cy="20%"
          r="200"
          stroke="oklch(0.75 0.15 210)"
          strokeWidth="1"
          fill="none"
          opacity="0.08"
        />
        
        {/* Circular arc - bottom left */}
        <circle
          cx="20%"
          cy="80%"
          r="300"
          stroke="oklch(0.95 0.25 110)"
          strokeWidth="1.5"
          fill="none"
          opacity="0.1"
        />
      </svg>
    </div>
  );
}
