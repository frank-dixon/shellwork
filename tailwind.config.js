/** Shellwork — eggshell paper / ink / Ameraucana blue-green → Marans brown */
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
          DEFAULT: "#9C5634",
          deep: "#7A3E22",
          soft: "#e8a08c",
        },
        teal: {
          DEFAULT: "#3A7263",
          bright: "#4C8A78",
          mist: "#dde9e2",
        },
      },
      fontFamily: {
        display: ["Michroma", '"IBM Plex Sans"', "system-ui", "sans-serif"],
        sans: ['"IBM Plex Sans"', "system-ui", "sans-serif"],
        mono: ['"IBM Plex Mono"', "ui-monospace", "monospace"],
      },
      boxShadow: {
        scene: "0 22px 48px rgba(28, 25, 22, 0.12)",
        soft: "0 10px 28px rgba(28, 25, 22, 0.08)",
      },
      keyframes: {
        drift: {
          "0%, 100%": { transform: "translate3d(0, 0, 0) rotate(0deg)" },
          "50%": { transform: "translate3d(12px, -18px, 0) rotate(4deg)" },
        },
        floaty: {
          "0%, 100%": { transform: "translateY(0) scale(1)" },
          "50%": { transform: "translateY(-22px) scale(1.04)" },
        },
        haze: {
          "0%, 100%": { opacity: "0.35", transform: "translateX(0)" },
          "50%": { opacity: "0.55", transform: "translateX(24px)" },
        },
      },
      animation: {
        drift: "drift 18s ease-in-out infinite",
        floaty: "floaty 14s ease-in-out infinite",
        haze: "haze 22s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
