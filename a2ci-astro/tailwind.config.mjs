/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'a2ci-red': '#C00000',
        'a2ci-black': '#000000',
        'a2ci-grey': '#DEDEDD',
        'bg-dark': '#0b0b0b',
        'card-dark': '#111111',
        'border-dark': '#222222',
      },
      fontFamily: {
        heading: ['Calibri', 'Candara', 'Segoe UI', 'Segoe', 'Optima', 'Arial', 'sans-serif'],
        body: ['Calibri', 'Candara', 'Segoe UI', 'Segoe', 'Optima', 'Arial', 'sans-serif'],
      },
      maxWidth: {
        'site': '1440px',
        'content': '1150px',
      },
    },
  },
  plugins: [],
};
