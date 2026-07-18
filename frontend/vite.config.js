import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],

  server: {
    port: 5173,

    proxy: {
      "/cost": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/prediction": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/analytics": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/sync": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/budget": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/anomaly": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/optimize": { target: "http://127.0.0.1:8000", changeOrigin: true },

    },
  },
});