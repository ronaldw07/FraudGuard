// Author: Ronald Wen
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0a0f1e',
          800: '#0d1526',
          700: '#111d35',
          600: '#162244',
        },
      },
    },
  },
  plugins: [],
}
