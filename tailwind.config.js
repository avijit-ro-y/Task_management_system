/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",    //templates inside root
    "./**/templates/**/*.html", //templates inside app
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

