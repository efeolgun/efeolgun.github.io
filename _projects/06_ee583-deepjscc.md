---
layout: page
title: "SNR-adaptive deep joint source-channel coding"
description: "A neural encoder and decoder that map images straight to channel symbols, with one model that adapts to the channel SNR so quality degrades gracefully."
importance: 6
category: wireless communications
---

<table class="efe-meta"><tbody><tr><th>Course</th><td>EE 583 Special Topics: Deep Learning (graduate course)</td></tr><tr><th>Term</th><td>Fall 2026, Boğaziçi University</td></tr><tr><th>Team</th><td>Individual</td></tr><tr><th>Status</th><td>In progress</td></tr><tr><th>Areas</th><td>wireless communications, machine learning</td></tr></tbody></table>
<p>Conventional systems compress an image and then protect it with a channel code designed for one SNR, so the image is lost below that SNR (the cliff effect). This project reimplements deep joint source-channel coding (DeepJSCC) in PyTorch and adds the SNR-adaptive attention modules of ADJSCC, so that one network works over a range of SNRs. Final report due December 2026.</p>
<p class="efe-links"><a class="btn btn-sm z-depth-0 efe-btn" href="https://efeolgun.github.io/coursework/2026-fall-EE583-deepjscc/proposal.pdf" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> Proposal</a></p>
