# Euchre Frontend

The frontend is built with Svelte. For production deployment, we use vite to
build the static files, and serve them in a continer using `Nginx`. For Local
development, vite can be used to serve the frontend directly.

## Local Setup
```bash
npm install
cp ../.env.local ./.env && npm run dev
```
