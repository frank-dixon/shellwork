/** Shellwork — cream shell / ink / terracotta */
module.exports = {
  content: ["./docs/**/*.{html,js}", "./src/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        cream: {
          DEFAULT: "#f6f0e6",
          deep: "#ebe2d4",
          paper: "#fffaf3",
        },
        ink: {
          DEFAULT: "#1c1916",
          soft: "#3d3833",
          mute: "#6b645c",
        },
        terra: {
          DEFAULT: "#c45c3e",
          deep: "#9a3f28",
          soft: "#e8a08c",
        },
        teal: {
          DEFAULT: "#2f6f66",
          bright: "#3d9e8f",
          mist: "#d5ebe6",
        },
      },
      fontFamily: {
        display: ['"Fraunces"', "Georgia", "serif"],
        sans: ['"Source Sans 3"', "system-ui", "sans-serif"],
      },
      boxShadow: {
        page: "0 18px 40px rgba(28, 25, 22, 0.18)",
        leaf: "-8px 0 24px rgba(28, 25, 22, 0.22)",
      },
      transitionTimingFunction: {
        flip: "cubic-bezier(0.22, 0.61, 0.36, 1)",
      },
    },
  },
  plugins: [],
};
