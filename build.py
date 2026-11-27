#!/usr/bin/env python3
"""Build index.html from projects.json.

Usage:  python3 build.py
Edit projects.json to add or change a project, then run this again.
The styles in style.css are inlined into the page.

Local preview with the PDFs from the coursework folder:
    FILES_BASE=/coursework/ python3 build.py
    python3 -m http.server 8790
"""
import html
import json
import os
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
E = html.escape
if os.environ.get("FILES_BASE"):
    DATA["files_base"] = os.environ["FILES_BASE"]


# ---------- links ----------

def link_url(item, link):
    if "url" in link:
        return link["url"]
    if link.get("code"):
        return DATA["code_base"] + item["folder"]
    return DATA["files_base"] + item["folder"] + "/" + link["file"]


def link_kind(link):
    """Short hint shown next to the label, so readers know what opens."""
    if link.get("file", "").endswith(".pdf"):
        return "PDF"
    if link.get("code") or "github.com" in link.get("url", ""):
        return "GitHub"
    return ""


def buttons(item):
    """Link buttons. The accessible name adds the item's title, so that
    screen readers do not hear a list of identical "Report" links."""
    out = []
    for l in item.get("links", []):
        kind = link_kind(l)
        kind_html = f' <span class="kind">{kind}</span>' if kind else ""
        name = f'{l["label"]} {kind}'.strip() + ": " + item.get("title", item.get("org", ""))
        aria = f' aria-label="{E(name)}"'
        out.append(f'<a class="btn" href="{E(link_url(item, l))}"{aria}>{E(l["label"])}{kind_html}</a>')
    return f'<div class="links">{"".join(out)}</div>' if out else ""


def status(item):
    return '<span class="badge">In progress</span>' if item.get("status") == "in progress" else ""


# ---------- sections ----------

def featured_item(p, n):
    fig = ""
    if p.get("image"):
        src = DATA["files_base"] + p["folder"] + "/" + p["image"]
        fig = f'''
      <figure>
        <img src="{E(src)}" width="1600" height="1333" loading="lazy"
             alt="An original and a restored film frame side by side, with the noise power spectrum of each below.">
        <figcaption>Original and restored frame (top) and their power spectra (bottom).</figcaption>
      </figure>'''
    return f'''
  <article class="feature" id="{E(p["id"])}">
    <div class="rail">
      <p class="num" aria-hidden="true">{n:02d}</p>
      <p class="when">{E(p["term"])}</p>
      <p class="where">{E(p["school"])}</p>
      <p class="course">{E(p["course"])}</p>
      {status(p)}
    </div>
    <div class="main">
      <h3>{E(p["title"])}</h3>
      <p class="desc">{E(p["summary"])}</p>
      {buttons(p)}
      <p class="team">{E(p["team"])}</p>{fig}
    </div>
  </article>'''


def project_row(p):
    return f'''
  <li class="row" id="{E(p["id"])}" data-areas="{E(" ".join(p["areas"]))}">
    <div class="rail">
      <p class="when">{E(p["term"])}</p>
      <p class="where">{E(p["school"])}</p>
      {status(p)}
    </div>
    <div class="main">
      <h3>{E(p["title"])}</h3>
      <p class="oneliner">{E(p["oneliner"])}</p>
      <p class="course">{E(p["course"])} <span class="team">· {E(p["team"])}</span></p>
    </div>
    <div class="files">{buttons(p) or '<p class="nofiles">No files yet</p>'}</div>
  </li>'''


def term_order(p):
    """Sort key for "Fall 2026" style terms: year, then Spring < Summer < Fall."""
    season, year = p["term"].split()
    return int(year), ["Spring", "Summer", "Fall"].index(season)


def course_key(name):
    m = re.match(r"([A-Z]+ ?\d{3})", name)
    return m.group(1).replace(" ", "") if m else name.lower()


def coursework():
    by_course = {}
    for p in DATA["projects"]:
        by_course[course_key(p["course"])] = p["id"]
    alias = {"st7 smart cities (with project)": "cs-st7-llm-telecom", "s8 project": "cs-s8-dirgnn-cio",
             "maintenance and industry 4.0": "cs-predictive-maintenance",
             "audio signal processing": "cs-room-acoustics"}
    rows = []
    for t in DATA["terms"]:
        items = []
        for c in t["courses"]:
            m = re.match(r"([A-Z]+ \d{3})\s+(.*)", c)
            code, name = (m.group(1), m.group(2)) if m else ("", c)
            name = name.replace(" (with project)", "")
            inner = f'<span class="code">{E(code)}</span><span class="cname">{E(name)}</span>'
            pid = alias.get(c.lower()) or by_course.get(course_key(c))
            if pid:
                items.append(f'<li><a href="#{E(pid)}">{inner}</a></li>')
            else:
                items.append(f'<li>{inner}</li>')
        if items:
            body = f'<ul class="courses">{"".join(items)}</ul>'
        else:
            body = f'<p class="gap"><a href="#experience">{E(t["where"])}</a></p>'
        where = f'<p class="where">{E(t["where"])}</p>' if items else ""
        rows.append(f'''
  <div class="term">
    <div class="rail"><p class="when">{E(t["term"])}</p>{where}</div>
    <div class="main">{body}</div>
  </div>''')
    return "".join(rows)


def experience():
    out = []
    for x in DATA["experience"]:
        out.append(f'''
  <article class="entry">
    <div class="rail"><p class="when">{E(x["term"])}</p></div>
    <div class="main">
      <h3>{E(x["org"])}</h3>
      <p class="role">{E(x["role"])}</p>
      <p>{E(x["summary"])}</p>
      {buttons(x)}
    </div>
  </article>''')
    return "".join(out)


def earlier():
    out = []
    for x in DATA["earlier"]:
        img = ""
        if x.get("image"):
            src = DATA["files_base"] + x["folder"] + "/" + x["image"]
            img = (f'<img class="photo" src="{E(src)}" width="256" height="275" loading="lazy" '
                   f'alt="Microplastic and water mixture in a beaker">')
        out.append(f'''
  <article class="entry">
    <div class="rail"><p class="when">{E(x["term"])}</p><p class="where">{E(x["school"])}</p>{img}</div>
    <div class="main">
      <h3>{E(x["title"])}</h3>
      <p class="award">{E(x["awards"])}</p>
      <p>{E(x["summary"])}</p>
      <p class="team">{E(x["team"])}</p>
      {buttons(x)}
    </div>
  </article>''')
    return "".join(out)


SCRIPT = """
(function () {
  var rows = Array.prototype.slice.call(document.querySelectorAll('#project-list .row'));
  var btns = Array.prototype.slice.call(document.querySelectorAll('.filter'));
  var count = document.getElementById('project-count');
  function show(area) {
    var n = 0;
    btns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.area === area)); });
    rows.forEach(function (r) {
      var on = area === 'all' || r.dataset.areas.split(' ').indexOf(area) >= 0;
      r.hidden = !on;
      if (on) n++;
    });
    count.textContent = 'Showing ' + n + ' of ' + rows.length + ' projects. Featured projects are not included.';
  }
  btns.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.area); }); });
  // A link to a project (for example from the coursework list) must not land on a hidden row.
  function reveal(id) {
    var el = id && document.getElementById(id);
    if (!el || !el.matches('.row, .feature')) return;  // section links (#projects) are not projects
    if (el.hidden) show('all');
    var d = el.querySelector('details');
    if (d) d.open = true;
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (a) reveal(decodeURIComponent(a.getAttribute('href').slice(1)));
  });
  reveal(decodeURIComponent(location.hash.slice(1)));
  window.addEventListener('beforeprint', function () {
    show('all');
    document.querySelectorAll('.feature details').forEach(function (d) { d.open = true; });
  });
})();
"""


def page():
    person = DATA["person"]
    featured = [p for p in DATA["projects"] if p.get("featured")]
    others = sorted((p for p in DATA["projects"] if not p.get("featured")), key=term_order, reverse=True)

    counts = {k: sum(k in p["areas"] for p in others) for k in DATA["areas"]}
    filters = f'<button type="button" class="filter" data-area="all" aria-pressed="true">All <span>{len(others)}</span></button>'
    filters += "".join(
        f'<button type="button" class="filter" data-area="{k}" aria-pressed="false">{E(v)} <span>{counts[k]}</span></button>'
        for k, v in DATA["areas"].items() if counts[k])

    cv = next((l for l in person["links"] if l["label"] == "CV"), None)
    plinks = "".join(
        f'<a class="btn{" primary" if l is cv else ""}" href="{E(l["url"])}">'
        f'{"Download CV" if l is cv else E(l["label"])}{" <span class=kind>PDF</span>" if l is cv else ""}</a>'
        for l in sorted(person["links"], key=lambda l: l is not cv))  # CV first
    facts = "".join(f'<div><dt>{E(f["label"])}</dt><dd>{E(f["text"])}</dd></div>' for f in person.get("facts", []))
    cv_nav = f'<a class="nav-cv" href="{E(cv["url"])}">CV</a>' if cv else ""
    css = (ROOT / "style.css").read_text(encoding="utf-8")

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(person["name"])} · {E(person["headline"])}</title>
<meta name="description" content="{E(person["summary"])}">
<meta name="color-scheme" content="light dark">
<script>document.documentElement.className = 'js';</script>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#featured">Skip to projects</a>

<nav class="bar" aria-label="Sections">
  <div class="wrap bar-in">
    <a class="bar-name" href="#top">{E(person["name"])}</a>
    <div class="bar-links">
      <a href="#featured">Featured</a>
      <a href="#projects">Projects</a>
      <a href="#experience">Experience</a>
      <a href="#coursework">Coursework</a>
      <a href="#earlier">Earlier</a>
    </div>
    {cv_nav}
  </div>
</nav>

<header class="hero" id="top">
  <div class="wrap hero-in">
    <div>
      <h1>{E(person["name"])}</h1>
      <p class="lede">{E(person["summary"])}</p>
      <div class="links hero-links">{plinks}</div>
    </div>
    <dl class="facts">{facts}</dl>
  </div>
</header>

<main>
<section id="featured" class="band" aria-labelledby="h-featured">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-featured">Featured projects</h2>
      <p>Selected work, newest first.</p>
    </div>
    {"".join(featured_item(p, i + 1) for i, p in enumerate(featured))}
  </div>
</section>

<section id="projects" class="wrap" aria-labelledby="h-projects">
  <div class="sec-head">
    <h2 id="h-projects">Other projects</h2>
    <p>Course projects from Boğaziçi University and CentraleSupélec, newest first.</p>
  </div>
  <div class="filters" role="group" aria-label="Filter projects by area">{filters}</div>
  <p class="count" id="project-count" aria-live="polite">Showing {len(others)} of {len(others)} projects. Featured projects are not included.</p>
  <div class="list-head" aria-hidden="true"><span>Term</span><span>Project</span><span>Files</span></div>
  <ol class="list" id="project-list">{"".join(project_row(p) for p in others)}
  </ol>
</section>

<section id="experience" class="wrap" aria-labelledby="h-experience">
  <div class="sec-head"><h2 id="h-experience">Experience</h2></div>
  {experience()}
</section>

<section id="coursework" class="wrap" aria-labelledby="h-coursework">
  <div class="sec-head">
    <h2 id="h-coursework">Coursework by semester</h2>
    <p>Underlined courses link to their project on this page. Homework solutions are not published, so that future students cannot copy them.</p>
  </div>
  {coursework()}
</section>

<section id="earlier" class="wrap" aria-labelledby="h-earlier">
  <div class="sec-head"><h2 id="h-earlier">Earlier work</h2><p>High school research.</p></div>
  {earlier()}
</section>
</main>

<footer>
  <div class="wrap">
    <p>Reports, slides and code: <a href="https://github.com/efeolgun/coursework">github.com/efeolgun/coursework</a></p>
    <p>Updated {date.today():%B %Y}.</p>
  </div>
</footer>
<script>{SCRIPT}</script>
</body>
</html>
'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(), encoding="utf-8")
    print("wrote", ROOT / "index.html")
