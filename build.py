#!/usr/bin/env python3
"""Build index.html from projects.json.

Usage:  python3 build.py
Edit projects.json to add or change a project, then run this again.
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
if os.environ.get("FILES_BASE"):  # local preview: FILES_BASE=/coursework/ python3 build.py
    DATA["files_base"] = os.environ["FILES_BASE"]


def link_url(item, link):
    if "url" in link:
        return link["url"]
    if link.get("code"):
        return DATA["code_base"] + item["folder"]
    return DATA["files_base"] + item["folder"] + "/" + link["file"]


def links_html(item):
    out = []
    for l in item.get("links", []):
        out.append(f'<a class="btn" href="{E(link_url(item, l))}">{E(l["label"])}</a>')
    return f'<div class="links">{"".join(out)}</div>' if out else ""


def badge(item):
    return '<span class="badge">In progress</span>' if item.get("status") == "in progress" else ""


def project_card(p, featured=False):
    areas = " ".join(p["areas"])
    area_tags = "".join(f'<span class="tag">{E(DATA["areas"][a])}</span>' for a in p["areas"])
    img = ""
    if p.get("image"):
        src = DATA["files_base"] + p["folder"] + "/" + p["image"]
        img = f'<img class="thumb" src="{E(src)}" alt="" loading="lazy">'
    cls = "card featured" if featured else "card"
    return f'''
<article class="{cls}" id="{E(p["id"])}" data-areas="{E(areas)}">
  {img}
  <div class="meta"><span>{E(p["term"])}</span><span>{E(p["school"])}</span>{badge(p)}</div>
  <h3>{E(p["title"])}</h3>
  <p class="course">{E(p["course"])}</p>
  <p>{E(p["summary"])}</p>
  <p class="team">{E(p["team"])}</p>
  <div class="foot">{links_html(p)}<div class="tags">{area_tags}</div></div>
</article>'''


def course_key(name):
    m = re.match(r"([A-Z]+ ?\d{3})", name)
    return m.group(1).replace(" ", "") if m else name.lower()


def term_rows():
    by_course = {}
    for p in DATA["projects"]:
        by_course[course_key(p["course"])] = p["id"]
        by_course[p["course"].lower()] = p["id"]
    alias = {"st7 smart cities (with project)": "cs-st7-llm-telecom", "s8 project": "cs-s8-dirgnn-cio",
             "maintenance and industry 4.0": "cs-predictive-maintenance",
             "audio signal processing": "cs-room-acoustics"}
    rows = []
    for t in DATA["terms"]:
        chips = []
        for c in t["courses"]:
            pid = alias.get(c.lower()) or by_course.get(course_key(c))
            if pid:
                chips.append(f'<a class="chip has" href="#{E(pid)}">{E(c)}</a>')
            else:
                chips.append(f'<span class="chip">{E(c)}</span>')
        body = f'<div class="chips">{"".join(chips)}</div>' if chips else ""
        rows.append(f'''
<div class="term">
  <div class="when">{E(t["term"])}</div>
  <div><p class="where">{E(t["where"])}</p>{body}</div>
</div>''')
    return "".join(rows)


def experience():
    out = []
    for x in DATA["experience"]:
        out.append(f'''
<div class="xp">
  <div class="when">{E(x["term"])}</div>
  <div><h3>{E(x["org"])}</h3><p class="course">{E(x["role"])}</p><p>{E(x["summary"])}</p>{links_html(x)}</div>
</div>''')
    return "".join(out)


def earlier():
    out = []
    for x in DATA["earlier"]:
        img = ""
        if x.get("image"):
            img = f'<img class="side" src="{E(DATA["files_base"] + x["folder"] + "/" + x["image"])}" alt="Microplastic and water mixture in a beaker" loading="lazy">'
        out.append(f'''
<article class="card wide">
  {img}
  <div>
    <div class="meta"><span>{E(x["term"])}</span><span>{E(x["school"])}</span></div>
    <h3>{E(x["title"])}</h3>
    <p class="award">{E(x["awards"])}</p>
    <p>{E(x["summary"])}</p>
    <p class="team">{E(x["team"])}</p>
    {links_html(x)}
  </div>
</article>''')
    return "".join(out)


def page():
    person = DATA["person"]
    featured = [p for p in DATA["projects"] if p.get("featured")]
    others = [p for p in DATA["projects"] if not p.get("featured")]
    filters = "".join(f'<button class="filter" data-area="{k}">{E(v)}</button>' for k, v in DATA["areas"].items())
    plinks = " ".join(f'<a href="{E(l["url"])}">{E(l["label"])}</a>' for l in person["links"])
    css = (ROOT / "style.css").read_text(encoding="utf-8")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(person["name"])}: academic portfolio</title>
<meta name="description" content="{E(person["summary"])}">
<style>{css}</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <p class="kicker">Academic portfolio</p>
    <h1>{E(person["name"])}</h1>
    <p class="headline">{E(person["headline"])}</p>
    <p class="lede">{E(person["summary"])}</p>
    <p class="plinks">{plinks}</p>
    <nav><a href="#featured">Featured</a><a href="#projects">All projects</a><a href="#coursework">Coursework</a><a href="#experience">Experience</a><a href="#earlier">Earlier work</a></nav>
  </div>
</header>
<main class="wrap">
  <section id="featured">
    <h2>Featured</h2>
    <div class="grid two">{"".join(project_card(p, True) for p in featured)}</div>
  </section>
  <section id="projects">
    <h2>All course projects</h2>
    <div class="filters"><button class="filter on" data-area="all">All</button>{filters}</div>
    <div class="grid three">{"".join(project_card(p) for p in others)}</div>
  </section>
  <section id="coursework">
    <h2>Coursework by semester</h2>
    <p class="note">Linked courses have a project on this page. Homework solutions are not published, so that future students cannot copy them.</p>
    {term_rows()}
  </section>
  <section id="experience">
    <h2>Experience</h2>
    {experience()}
  </section>
  <section id="earlier">
    <h2>Earlier work</h2>
    {earlier()}
  </section>
</main>
<footer class="wrap">
  <p>Reports, slides and code: <a href="https://github.com/efeolgun/coursework">github.com/efeolgun/coursework</a>. Updated {date.today():%B %Y}.</p>
</footer>
<script>
document.querySelectorAll('.filter').forEach(b => b.addEventListener('click', () => {{
  document.querySelectorAll('.filter').forEach(x => x.classList.toggle('on', x === b));
  const a = b.dataset.area;
  document.querySelectorAll('#projects .card').forEach(c => {{
    c.hidden = !(a === 'all' || c.dataset.areas.split(' ').includes(a));
  }});
}}));
</script>
</body>
</html>
'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(), encoding="utf-8")
    print("wrote", ROOT / "index.html")
