/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EEF2FF',
          100: '#E0E7FF',
          200: '#C7D2FE',
          300: '#A5B4FC',
          400: '#818CF8',
          500: '#6366F1',
          600: '#4F46E5',
          700: '#4338CA',
          800: '#3730A3',
          900: '#312E81',
        },
        secondary: {
          50: '#ECFDF5',
          100: '#D1FAE5',
          200: '#A7F3D0',
          300: '#6EE7B7',
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
          700: '#047857',
          800: '#065F46',
          900: '#064E3B',
        },
        accent: {
          50: '#F5F3FF',
          100: '#EDE9FE',
          200: '#DDD6FE',
          300: '#C4B5FD',
          400: '#A78BFA',
          500: '#8B5CF6',
          600: '#7C3AED',
          700: '#6D28D9',
          800: '#5B21B6',
          900: '#4C1D95',
        },
      },
      fontFamily: {
        sans: ['Montserrat', 'sans-serif'],
        mono: ['Fira Code', 'Monaco', 'Courier New', 'monospace'],
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      },
    },
  },
  variants: {
    extend: {
      visibility: ['group-hover'],
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    plugin(function ({ addUtilities }) {  
      const newUtilities = {  
        '.hide-scrollbar::-webkit-scrollbar': {  
          display: 'none',  
        },
        '.hide-scrollbar:hover::-webkit-scrollbar': {  
          display: 'block',  
        },
        '.hide-scrollbar': {  
          '-ms-overflow-style': 'none',  
          'scrollbar-width': 'none',  
        },  
        '.hide-scrollbar:hover': {  
          '-ms-overflow-style': 'auto',  
          'scrollbar-width': 'auto',  
        },
      }  
      addUtilities(newUtilities, ['responsive'])  
    }),
  ],
  important: true
};
