/** @type {import('tailwindcss').Config} */
// TaskMaster Pro - TailwindCSS Configuration
// Generated with GitHub Copilot assistance
// Mobile-first responsive design per Constitution Principle IV

module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      // Mobile-first breakpoints (Constitution Principle IV)
      screens: {
        'xs': '375px',   // Minimum supported viewport
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
      // Minimum touch target size: 44x44px (Constitution Principle IV)
      minHeight: {
        'touch': '44px',
      },
      minWidth: {
        'touch': '44px',
      },
      // Task priority color scheme
      colors: {
        priority: {
          low: '#10b981',      // Green
          medium: '#f59e0b',   // Amber
          high: '#ef4444',     // Red
        },
        status: {
          pending: '#6b7280',       // Gray
          inProgress: '#3b82f6',    // Blue
          completed: '#10b981',     // Green
        },
      },
    },
  },
  plugins: [],
}
