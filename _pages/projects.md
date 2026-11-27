---
layout: page
title: projects
permalink: /projects/
description: Course, exchange and research projects. Each card opens a page with the summary, the team, and links to the report, slides and code.
nav: true
nav_order: 2
display_categories: ["wireless communications", "signal processing", "machine learning", "hardware", "other"]
horizontal: false
---

<div class="projects">
{% for category in page.display_categories %}
  <a id="{{ category | slugify }}" href=".#{{ category | slugify }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <div class="row row-cols-1 row-cols-md-3">
  {% for project in sorted_projects %}
    {% include projects.liquid %}
  {% endfor %}
  </div>
{% endfor %}
</div>
