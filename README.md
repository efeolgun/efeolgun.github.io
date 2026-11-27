# efeolgun.github.io

Academic portfolio of Efe Olgun, built with the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme.

## Change the content

The project, experience and coursework text lives in `_content/projects.json`.

1. Edit `_content/projects.json`.
2. Run `python3 _content/generate.py` from the repository root.
3. Commit and push to `main`.

The script writes `_pages/*.md`, `_projects/*.md` and `_data/socials.yml`. Do not edit those files by hand, because the next run overwrites them. Reports and code live in [efeolgun/coursework](https://github.com/efeolgun/coursework).

## CV files

- `assets/pdf/Efe_Olgun_CV_Europass.pdf` is the Europass CV. `cv.pdf` is a copy at the old address.
- `assets/pdf/Efe_Olgun_Resume.pdf` is the two-page résumé. `resume.pdf` is a copy at the old address.

The public copies do not contain the phone number. Replace all four files when a CV changes.

## Preview and deploy

To preview the site, run `docker compose up` and open http://localhost:8080.

A push to `main` starts the Deploy workflow. It builds the site into the `gh-pages` branch, and GitHub Pages serves that branch.

The old hand-written site is on the `legacy-static` branch.
