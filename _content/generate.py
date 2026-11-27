"""Generate the site pages from _content/projects.json.

Usage, from the repository root:  python3 _content/generate.py
It writes _pages/about.md, projects.md, coursework.md, cv.md, the files in
_projects/ and _data/socials.yml. Do not edit those files by hand: edit
projects.json and run this script again. If a sibling checkout of the
coursework repository exists, it also copies the project images.
"""
import html
import json
import pathlib
import sys

OUT = pathlib.Path(__file__).resolve().parent.parent
COURSEWORK = OUT.parent / "coursework"
D = json.loads((OUT / "_content" / "projects.json").read_text())
E = html.escape

AREA_ORDER = ["wireless", "signal", "ml", "hardware", "other"]
AREA_NAME = {
    "wireless": "wireless communications",
    "signal": "signal processing",
    "ml": "machine learning",
    "hardware": "hardware",
    "other": "other",
}


def link_url(item, link):
    if "url" in link:
        return link["url"]
    if link.get("code"):
        return D["code_base"] + item["folder"]
    return D["files_base"] + item["folder"] + "/" + link["file"]


def buttons(item):
    out = []
    for l in item.get("links", []):
        url = link_url(item, l)
        icon = "fa-brands fa-github" if ("github.com" in url) else "fa-solid fa-file-pdf" if url.endswith(".pdf") else "fa-solid fa-link"
        out.append(
            f'<a class="btn btn-sm z-depth-0 efe-btn" href="{E(url)}" target="_blank" rel="noopener">'
            f'<i class="{icon}"></i> {E(l["label"])}</a>'
        )
    return '<p class="efe-links">' + " ".join(out) + "</p>" if out else ""


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def meta(p):
    rows = [("Course", p["course"]), ("Term", p["term"] + ", " + p["school"]), ("Team", p["team"])]
    if p.get("status"):
        rows.append(("Status", p["status"].capitalize()))
    rows.append(("Areas", ", ".join(AREA_NAME[a] for a in p["areas"])))
    body = "".join(f"<tr><th>{E(k)}</th><td>{E(v)}</td></tr>" for k, v in rows)
    return f'<table class="efe-meta"><tbody>{body}</tbody></table>'


# ---------- projects collection ----------
order = sorted(D["projects"], key=lambda p: (not p.get("featured"), -int(p["term"].split()[-1]), p["term"].split()[0] != "Fall"))
images = {}
for i, p in enumerate(order, 1):
    img = ""
    if p.get("image"):
        name = pathlib.Path(p["image"]).name
        images[name] = COURSEWORK / p["folder"] / p["image"]
        img = f"assets/img/{name}"
    fm = [
        "---",
        "layout: page",
        f"title: {yaml_str(p['title'])}",
        f"description: {yaml_str(p['oneliner'])}",
        f"importance: {i}",
        f"category: {AREA_NAME[p['areas'][0]]}",
    ]
    if img:
        fm.append(f"img: {img}")
    fm.append("---")
    body = [meta(p), "", f"<p>{E(p['summary'])}</p>", buttons(p)]
    if img:
        body.append(
            "{% include figure.liquid loading=\"lazy\" path=\"" + img + "\" class=\"img-fluid rounded z-depth-1\" alt=\"Figure from the project\" %}"
        )
    write(f"_projects/{i:02d}_{p['id']}.md", "\n".join(fm) + "\n\n" + "\n".join(b for b in body if b) + "\n")

for e in D["earlier"]:
    name = pathlib.Path(e["image"]).name
    images[name] = COURSEWORK / e["folder"] / e["image"]

# ---------- about page ----------
P = D["person"]
facts = "".join(f"<tr><th>{E(f['label'])}</th><td>{E(f['text'])}</td></tr>" for f in P["facts"])
exp = []
for x in D["experience"]:
    exp.append(
        f'<div class="efe-entry"><p class="efe-when">{E(x["term"])}</p>'
        f'<h3>{E(x["role"])}, <span class="efe-org">{E(x["org"])}</span></h3>'
        f'<p>{E(x["summary"])}</p>{buttons(x) if x.get("links") else ""}</div>'
    )
featured = []
for i, p in enumerate(order, 1):
    if p.get("featured"):
        slug = f"{i:02d}_{p['id']}"
        featured.append(
            f'<li><a href="{{{{ \'/projects/{slug}/\' | relative_url }}}}">{E(p["title"])}</a>'
            f' <span class="efe-dim">({E(p["term"])}, {E(p["school"])})</span><br>{E(p["oneliner"])}</li>'
        )
earlier = []
for x in D["earlier"]:
    earlier.append(
        f'<div class="efe-entry"><p class="efe-when">{E(x["term"])}, {E(x["school"])}</p>'
        f'<h3>{E(x["title"])}</h3><p class="efe-dim">{E(x["team"])}</p>'
        f'<p><strong>{E(x["awards"])}</strong></p><p>{E(x["summary"])}</p>{buttons(x)}'
        '{% include figure.liquid loading="lazy" path="assets/img/' + pathlib.Path(x["image"]).name
        + '" class="img-fluid rounded z-depth-1 efe-small" alt="Sponge and microplastic mixture from the experiment" %}</div>'
    )

about = f"""---
layout: about
title: about
permalink: /
subtitle: {yaml_str(P['headline'])}
social: true
announcements:
  enabled: false
latest_posts:
  enabled: false
selected_papers: false
---

<p class="efe-lead">{E(P['summary'])}</p>

<table class="efe-facts"><tbody>{facts}</tbody></table>

<p class="efe-cta">
<a class="btn efe-btn efe-primary" href="{{{{ '/cv/' | relative_url }}}}"><i class="fa-solid fa-file-lines"></i> CV (Europass)</a>
<a class="btn efe-btn" href="{{{{ '/assets/pdf/Efe_Olgun_Resume.pdf' | relative_url }}}}" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> Résumé (2 pages)</a>
</p>

## experience

{''.join(exp)}

## selected projects

<ul class="efe-featured">{''.join(featured)}</ul>

<p><a href="{{{{ '/projects/' | relative_url }}}}">All {len(order)} projects</a>, grouped by area. <a href="{{{{ '/courses/' | relative_url }}}}">All courses</a>, by term.</p>

## earlier work

{''.join(earlier)}
"""
write("_pages/about.md", about)

# ---------- projects page ----------
cats = [AREA_NAME[a] for a in AREA_ORDER if any(p["areas"][0] == a for p in order)]
projects_page = f"""---
layout: page
title: projects
permalink: /projects/
description: Course, exchange and research projects. Each card opens a page with the summary, the team, and links to the report, slides and code.
nav: true
nav_order: 2
display_categories: {json.dumps(cats)}
horizontal: false
---

<div class="projects">
{{% for category in page.display_categories %}}
  <a id="{{{{ category | slugify }}}}" href=".#{{{{ category | slugify }}}}">
    <h2 class="category">{{{{ category }}}}</h2>
  </a>
  {{% assign categorized_projects = site.projects | where: "category", category %}}
  {{% assign sorted_projects = categorized_projects | sort: "importance" %}}
  <div class="row row-cols-1 row-cols-md-3">
  {{% for project in sorted_projects %}}
    {{% include projects.liquid %}}
  {{% endfor %}}
  </div>
{{% endfor %}}
</div>
"""
write("_pages/projects.md", projects_page)

# ---------- coursework page ----------
terms = []
for t in D["terms"]:
    items = "".join(f"<li>{E(c)}</li>" for c in t["courses"])
    terms.append(
        f'<div class="efe-entry"><h3>{E(t["term"])}</h3><p class="efe-dim">{E(t["where"])}</p>'
        + (f"<ul>{items}</ul>" if items else "")
        + "</div>"
    )
write(
    "_pages/courses.md",
    f"""---
layout: page
title: courses
permalink: /courses/
description: Courses by term, newest first.
nav: true
nav_order: 3
---

{''.join(terms)}
""",
)

# ---------- CV page ----------
write(
    "_pages/cv.md",
    """---
layout: page
title: CV
permalink: /cv/
nav: true
nav_order: 4
description: My CV in the Europass format, and a two-page résumé.
---

<p class="efe-cta">
<a class="btn efe-btn efe-primary" href="{{ '/assets/pdf/Efe_Olgun_CV_Europass.pdf' | relative_url }}" target="_blank" rel="noopener"><i class="fa-solid fa-download"></i> Europass CV (PDF)</a>
<a class="btn efe-btn" href="{{ '/assets/pdf/Efe_Olgun_Resume.pdf' | relative_url }}" target="_blank" rel="noopener"><i class="fa-solid fa-download"></i> Résumé, 2 pages (PDF)</a>
</p>

<object class="efe-pdf" data="{{ '/assets/pdf/Efe_Olgun_CV_Europass.pdf' | relative_url }}" type="application/pdf">
<p>Your browser cannot show the PDF here. <a href="{{ '/assets/pdf/Efe_Olgun_CV_Europass.pdf' | relative_url }}">Open the Europass CV</a>.</p>
</object>
""",
)

# ---------- socials ----------
write(
    "_data/socials.yml",
    """# Social links shown on the about page.
email: efeolgunn@hotmail.com
github_username: efeolgun
linkedin_username: efe-olgun
""",
)

# ---------- images ----------
import shutil

for name, src in images.items():
    if src.exists():
        shutil.copy(src, OUT / "assets/img" / name)
    elif not (OUT / "assets/img" / name).exists():
        print("missing image:", name)
print("projects:", len(order), "images:", list(images))
