# AI & Robotics Portfolio

A fast, responsive, and accessible portfolio site tailored for an AI & Robotics Engineer. Built with plain HTML/CSS/JS (no external dependencies), including dark mode, project cards, publications, and contact links.

## Structure

- `index.html` — Main page markup
- `src/layout/*` — Head/foot wrappers (`start.html`, `end.html`)
- `src/sections/*` — Section partials (home, about, skills, projects, education, experience, publications, contact)
- `assets/css/styles.css` — Theme, layout, and components
- `assets/js/main.js` — Dark mode, mobile nav, reveal animations
- `assets/img/*` — Local SVG artwork and favicon
- `assets/resume/` — Put your resume PDF here
 - `scripts/build.py` — Concatenates partials into `index.html`

## Quick Start

1. Open `index.html` in a browser.
2. Replace placeholder links and text (GitHub, LinkedIn, email, location, company names).
3. Drop your resume at `assets/resume/Akash_Bhansali_Resume.pdf` or update the Resume link in the header.

## Build from Partials

- Edit files in `src/layout/` and `src/sections/`.
- Rebuild `index.html` by running:

  `python3 scripts/build.py`

This concatenates the section files in order into the root `index.html`.

## Customize

- Name, title, and description: edit `<title>`, meta description, and hero section in `index.html`.
- Social links: update GitHub/LinkedIn/email in `index.html`.
- Projects: add/remove `<article class="card">` blocks in `#projects` with your details.
- Experience: edit the timeline items in `#experience`.
- Publications: update the list in `#publications`.
- Colors: tweak CSS variables in `assets/css/styles.css`.
- Dark mode: toggled via the moon/sun button; persists in `localStorage`.

## Deploy

### GitHub Pages (with Actions)

This repo includes a workflow that builds from partials and deploys automatically.

1. Create a new GitHub repository and push this project (set default branch to `main`).
2. Ensure Actions are enabled for the repo.
3. On the first push to `main`, the workflow `.github/workflows/deploy.yml` runs:
   - Builds `index.html` from `src/` partials
   - Publishes the site to GitHub Pages
4. In GitHub: Settings → Pages → Check the deployed URL (it appears after the first run).

Notes
- Site URL: `https://<username>.github.io/<repo>` (or `https://<username>.github.io` if the repo is named `<username>.github.io`).
- Edit partials in `src/` and push; the workflow rebuilds and redeploys automatically.
- A `.nojekyll` file is included to prevent Jekyll processing.

### Other static hosts

Any static host (Netlify, Vercel, S3, Firebase Hosting) works. If you use CI, run `python3 scripts/build.py` before uploading.

## Notes

- The site avoids external fonts or libraries to keep it fast and offline‑friendly.
- Images are simple SVG placeholders — replace with real screenshots/photos as desired.
- For SEO, update the JSON‑LD `@type: Person` block in `index.html` with your actual profile URLs.

## License

You own the content you place in this portfolio. Use, modify, and deploy freely.
