---
title: "Research"
layout: page
permalink: /research/
math: true
---

# Research

{% for r in site.data.research %}
<div class="section-card">
<h2>{{ r.title }}</h2>
<p style="color: var(--text-secondary); font-style: italic;">{{ r.label | capitalize }} &middot; {{ r.location }} &middot; {{ r.dates }}</p>
{% for para in r.paragraphs %}
{{ para | markdownify }}
{% endfor %}
</div>
{% endfor %}
