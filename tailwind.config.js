/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**"],
  theme: {
    extend: {
      fontFamily: {
        "poppins": ["Poppins"]
      },
      "colors": {
        'text': '#0e0821',
        'background': '#ffffff',
        'primary': '#8365dc',
        'secondary': '#bfb0ed',
        'accent': '#4827aa',
      }
    },
  },
  plugins: [],
  script: "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
}

// npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch