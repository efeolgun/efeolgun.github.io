---
layout: page
title: "Directed GNNs for Cell Individual Offset tuning"
description: "An end-to-end loop from mobility simulation to a directed GNN that predicts risky handover edges and updates the CIO matrix. In the large environment it modifies 48 of 156 directed links."
importance: 2
category: wireless communications
---

<table class="efe-meta"><tbody><tr><th>Course</th><td>S8 research project (IoT track), CentraleSupélec</td></tr><tr><th>Term</th><td>Spring 2026, CentraleSupélec</td></tr><tr><th>Team</th><td>Team of five (A. Seigle, E. Olgun, N. Tüysüz, A. Ammour, A. Choquel)</td></tr><tr><th>Areas</th><td>wireless communications, machine learning</td></tr></tbody></table>
<p>An end-to-end loop that simulates users moving between base stations (Gymnasium mobile-env), extracts directed handover graphs, trains a directed GNN to predict risky handover edges, and updates the CIO matrix. The final version added independent failure labels, continuous severity metrics, weighted losses and numerical sanitization. In the large environment it modifies 48 of 156 directed links. This project became the starting point of my senior design project.</p>
<p class="efe-links"><a class="btn btn-sm z-depth-0 efe-btn" href="https://efeolgun.github.io/coursework/2026-spring-CS-S8-dirgnn-cio/report.pdf" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> Report</a> <a class="btn btn-sm z-depth-0 efe-btn" href="https://github.com/adrienseigle/DirGNN-for-CIO-finetunning" target="_blank" rel="noopener"><i class="fa-brands fa-github"></i> Team code</a></p>
