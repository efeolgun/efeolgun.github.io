---
layout: page
title: "Film grain across eras: spectral analysis and restoration"
description: "Noise spectra of films from 1925, 1963 and 1984, and an era-specific restoration pipeline for each, built because textbook spatial filters failed on real footage."
importance: 4
category: signal processing
img: assets/img/analysis_phantom.jpg
---

<table class="efe-meta"><tbody><tr><th>Course</th><td>EE 475 Introduction to Image Processing</td></tr><tr><th>Term</th><td>Fall 2025, Boğaziçi University</td></tr><tr><th>Team</th><td>Individual</td></tr><tr><th>Areas</th><td>signal processing</td></tr></tbody></table>
<p>Noise in a 1925 silent film, a 1963 film and a 1984 VHS-era film has different physics: impulse dirt and flicker, Gaussian grain, and tape hiss with chroma noise. The project measures the power spectral density of each and builds era-specific restoration pipelines with temporal filtering and color-space decomposition, because textbook spatial filters failed on real footage.</p>
<p class="efe-links"><a class="btn btn-sm z-depth-0 efe-btn" href="https://efeolgun.github.io/coursework/2025-fall-EE475-film-grain/report.pdf" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> Report</a> <a class="btn btn-sm z-depth-0 efe-btn" href="https://efeolgun.github.io/coursework/2025-fall-EE475-film-grain/slides.pdf" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> Slides</a> <a class="btn btn-sm z-depth-0 efe-btn" href="https://github.com/efeolgun/coursework/tree/main/2025-fall-EE475-film-grain" target="_blank" rel="noopener"><i class="fa-brands fa-github"></i> Code</a></p>
{% include figure.liquid loading="lazy" path="assets/img/analysis_phantom.jpg" class="img-fluid rounded z-depth-1" alt="Figure from the project" %}
