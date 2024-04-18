/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
  ],
  theme: {

    extend: {
      boxShadow: {
        'wooper': '0 25px 30px -10px rgba(0, 0, 0, 0.5)',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
  daisyui: {
    themes: [
      {
        wooper_dark:{
            "primary":"#323af0",
            "secondary": "#92e8c0",
            "accent": "#92e8c0",
            "neutral": "#f3f3f3",
            "neutral-content": "#f3f3f3",
            "base-100": "#292c36",
            "base-200": "#21242c",
            "base-300": "#16171c",
            "info": "#fffde3",
            "success": "#51b341",
            "warning": "#fff971",
            "error": "#ee3046",
        },
      },
      "light",
      "cupcake",
      "corporate"
    ],
    styled: true,
    base: true,
    utils: true,
    logs: true,
    rtl: false,
    logs: true,
    themeRoot: "root",
  }
}

