/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**"],
  theme: {
    extend: {

    },
  },
  plugins: [],
  script: "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
}

// npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch