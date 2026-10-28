---
title: "About"
layout: page
permalink: /about/
---

# About

<div class="section-card">
<div class="pi-card">
<div>
<h2 class="pi-name">{{ site.name }}</h2>
<p style="font-style: italic; color: var(--text-secondary);">{{ site.title }}, {{ site.institution }}</p>
<div class="pi-links">
{% if site.email %}<a href="mailto:{{ site.email }}" class="icon-link" title="Email" aria-label="Email">{% include icon.html name="envelope" %}</a>{% endif %}
{% if site.links.cv != "" %}<a href="{{ site.links.cv | prepend: '/' | relative_url }}" class="icon-link" title="CV" aria-label="CV">{% include icon.html name="cv" %}</a>{% endif %}
{% if site.links.google_scholar != "" %}<a href="{{ site.links.google_scholar }}" class="icon-link" title="Google Scholar" aria-label="Google Scholar">{% include icon.html name="google-scholar" %}</a>{% endif %}
{% if site.links.github != "" %}<a href="{{ site.links.github }}" class="icon-link" title="GitHub" aria-label="GitHub">{% include icon.html name="github" %}</a>{% endif %}
</div>
<p style="margin-top: var(--space-4);">
ORCID <a href="{{ site.links.orcid }}">0000-0002-9368-9120</a> &middot;
<a href="{{ site.links.inspire }}">INSPIRE-HEP</a>
</p>
</div>
</div>
</div>

<div class="section-card">
<h3>Education</h3>
<ul>
{% for e in site.data.education %}
<li><strong>{{ e.degree }}</strong>, {{ e.institution }}, {{ e.location }} ({{ e.dates }})<br>
<span style="color: var(--text-secondary);">Thesis: {{ e.thesis }}{% if e.status %} <em>{{ e.status }}</em>{% endif %}</span></li>
{% endfor %}
</ul>
</div>

<div class="section-card">
<h3>Positions</h3>
<ul>
{% for p in site.data.experience.positions %}
<li><strong>{{ p.title }}</strong>, {{ p.organization }}, {{ p.location }} ({{ p.dates }})</li>
{% endfor %}
</ul>
</div>

<div class="section-card">
<h3>Languages</h3>
<ul>
{% for l in site.data.skills.languages %}
<li><strong>{{ l.name }}</strong> — {{ l.level }}</li>
{% endfor %}
</ul>
</div>
