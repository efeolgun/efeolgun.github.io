---
layout: page
title: "Music pitch detection and auto-tuning"
description: "An auto-tuner for monophonic vocals with autocorrelation and cepstrum pitch detection and a phase vocoder. Center-clipped autocorrelation was the most stable on amateur recordings."
importance: 9
category: signal processing
---

<table class="efe-meta"><tbody><tr><th>Course</th><td>EE 473 Introduction to Digital Signal Processing</td></tr><tr><th>Term</th><td>Fall 2025, Boğaziçi University</td></tr><tr><th>Team</th><td>With Mert Karahan. My part: autocorrelation with center clipping, and the user interface.</td></tr><tr><th>Areas</th><td>signal processing</td></tr></tbody></table>
<p>A closed-loop auto-tuner for monophonic vocals. It detects the fundamental frequency frame by frame with autocorrelation and with the cepstrum, maps it to the nearest note, and shifts the pitch with a phase vocoder. Autocorrelation with center clipping gave the most stable results on amateur recordings.</p>
<p class="efe-links"><a class="btn btn-sm z-depth-0 efe-btn" href="https://efeolgun.github.io/coursework/2025-fall-EE473-pitch-detection-autotune/report.pdf" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> Report</a> <a class="btn btn-sm z-depth-0 efe-btn" href="https://efeolgun.github.io/coursework/2025-fall-EE473-pitch-detection-autotune/slides.pdf" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> Slides</a> <a class="btn btn-sm z-depth-0 efe-btn" href="https://github.com/efeolgun/coursework/tree/main/2025-fall-EE473-pitch-detection-autotune" target="_blank" rel="noopener"><i class="fa-brands fa-github"></i> Code</a></p>
