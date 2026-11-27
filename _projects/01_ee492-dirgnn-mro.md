---
layout: page
title: "Directed GNNs for mobility robustness optimization"
description: "Closed-loop tuning of the directed Cell Individual Offset matrix with a directed GNN. The simulator, rebuilt on the 3GPP documents, already reproduces the full MRO trade-off without tuning."
importance: 1
category: wireless communications
---

<table class="efe-meta"><tbody><tr><th>Course</th><td>EE 492 Senior Design Project</td></tr><tr><th>Term</th><td>Fall 2026, Boğaziçi University</td></tr><tr><th>Team</th><td>Individual project, principal investigator Prof. Mutlu Koca</td></tr><tr><th>Status</th><td>In progress</td></tr><tr><th>Areas</th><td>wireless communications, machine learning</td></tr></tbody></table>
<p>A handover moves a phone from one cell to another, and each cell keeps a Cell Individual Offset (CIO) for each neighbor. This project tunes that directed CIO matrix in a closed loop: a simulator labels every handover as normal, too late, too early or ping-pong, and a directed graph neural network learns the failure risk of each cell pair. The first half rebuilt the simulator, channel and failure labels on the 3GPP documents. The rebuilt simulator reproduces the full MRO trade-off without tuning. GNN training runs in the second half of the semester.</p>
