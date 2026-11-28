# efeolgun.github.io

Source of https://efeolgun.github.io, the academic page of Efe Olgun.

## Layout

- `public/` is the site. The deploy step publishes this folder as it is.
- `public/index.html` is built locally from `_content/projects.json`.
- `public/cv.pdf` and `public/resume.pdf` are the public CV and résumé.
- Old addresses (`/projects/...`, `/courses/`, `/cv/`) are small redirect pages in `public/`.
- `.github/workflows/deploy.yml` copies `public/` to the `gh-pages` branch on each push to `main` that changes `public/`.

The project files and reports are in the repository `efeolgun/coursework`.

The earlier al-folio version of the site is in the branch `al-folio-archive`.
