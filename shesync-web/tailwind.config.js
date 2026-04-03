export default {
  darkMode: "class",   // IMPORTANT

  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {
      colors: {
        primary: "#7C3AED",
        secondary: "#4F46E5",
        accent: "#EC4899",
      },
      boxShadow: {
        soft: "0 10px 30px rgba(0,0,0,0.05)",
      }
    },
  },

  plugins: [],
}