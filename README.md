# AI & Robotics Portfolio

Static portfolio for Akashkumar Jain, focused on AI & Robotics, Physical AI, Sim2Real systems, computer vision, foundation models, and deployable ML/robotics work.

The site is built with plain HTML, CSS, and JavaScript. There are no external frontend dependencies.

## Current Content

- Hero positioning for AI & Robotics, Physical AI, ROS, Isaac/MuJoCo simulation, VLA, LLM/VLM, ML, and computer vision.
- About section with interested areas, profile photo, contact details, and focus points.
- Skills grouped by programming, ML/AI, CV/multimodal, robotics/simulation, experimentation, and tools.
- Projects with filterable categories: ML, CV, Robotics, LLM / Multimodal, and Personal.
- Master's thesis card: `Improving Vision Transformer Efficiency Using Genetic Patch Pruning`.
- Education, experience, resume link, social links, and contact cards.

## Structure

- `index.html` - Generated site entry point.
- `src/layout/start.html` - Document head, metadata, header, navigation.
- `src/layout/end.html` - Footer and script entry.
- `src/sections/*.html` - Source partials for page sections.
- `assets/css/styles.css` - Theme, layout, responsive styles, cards, filters.
- `assets/js/app.js` - JavaScript entry point.
- `assets/js/modules/` - Theme, navigation, reveal effects, project filters.
- `assets/img/profile_pic.jpeg` - Profile photo used in the About card.
- `assets/img/*.svg` - Logo, favicon, hero, and project illustrations.
- `assets/resume/CV__Akashkumar_Jain.pdf` - Resume linked from the header and hero.
- `scripts/build.py` - Concatenates source partials into `index.html`.

## Local Preview

Because the JavaScript uses ES modules, preview through a local server:

```sh
python3 -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080/
```

## Editing Workflow

Edit the source files in `src/layout/` and `src/sections/`, then rebuild:

```sh
python3 scripts/build.py
```

Do not edit `index.html` directly for lasting content changes; it is generated from the partials.

## Common Updates

- Hero copy: `src/sections/home.html`
- About text and interested areas: `src/sections/about.html`
- Skills: `src/sections/skills.html`
- Projects and project filters: `src/sections/projects.html`
- Education and thesis mention: `src/sections/education.html`
- Experience: `src/sections/experience.html`
- Contact links: `src/sections/contact.html`
- SEO metadata and social preview text: `src/layout/start.html`
- Styling and responsive layout: `assets/css/styles.css`

## Deployment

This is a static site and can be hosted on GitHub Pages, Netlify, Vercel, S3, Firebase Hosting, or any static host.

Before deploying, rebuild `index.html`:

```sh
python3 scripts/build.py
```

This repository includes a GitHub Pages workflow in `.github/workflows/deploy.yml` that builds from the partials and publishes the generated site.

## Notes

- Keep project links real; avoid placeholder `href="#"` actions.
- Keep content changes in `src/` partials so the build remains reproducible.
- The site uses local assets and system fonts for fast loading.
