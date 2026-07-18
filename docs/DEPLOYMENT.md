# Deployment

This is a static HTML/CSS/JS site — no build step, no server, no bundler.
Vercel deploys the repository contents as-is using the rewrites in
[`vercel.json`](../vercel.json).

**No Vercel environment variables are required.** The Firebase web config
lives in [`assets/js/firebase-config.js`](../assets/js/firebase-config.js)
and is committed directly — Firebase web API keys are not secret; access
control is enforced by [Firestore Security Rules](../firestore.rules), not
by hiding the config. A static site's browser JS can't read `.env` files
anyway (that's a server/build-time mechanism this project doesn't have).

## Vercel project settings

- **Root Directory**: repo root (where `vercel.json` lives).
- **Framework Preset**: Other (no build command, no output directory —
  files are served directly).
- **Build Command**: none.
- **Environment Variables**: none.

## Routing

All page files live under `pages/` on disk but are served from the site
root via rewrites (e.g. `pages/about.html` → `/about.html`). Asset paths
inside each page use enough `../` to reach `assets/` from wherever the
file sits on disk; browsers clamp any `..` that would go above the URL
root, so this resolves correctly at every nesting depth without needing a
matching URL structure.

`/launch-list` (no extension) is explicitly rewritten to
`pages/launch-list.html` for the signup page. Every other page is reached
via its `.html` name (e.g. `/shop-all.html`).
