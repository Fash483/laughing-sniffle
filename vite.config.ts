import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  // Relative base so asset URLs work whether this is served from a GitHub
  // Pages project site (https://<user>.github.io/<repo>/) or a user/org
  // site (https://<user>.github.io/) or a custom domain.
  base: "./",
  plugins: [react()],
  server: {
    port: 5173,
  },
});
