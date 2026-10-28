---
title: "Projects"
layout: page
permalink: /projects/
---

# Projects

A few things I maintain in the open. Everything else is on
[GitHub]({{ site.links.github }}).

{% for project in site.data.projects %}
<div class="section-card" markdown="0">
<h2>{{ project.name }}</h2>
{% if project.repo or project.website or project.docs or project.paper %}
<div class="pub-actions" style="margin-bottom: var(--space-3);">
{% if project.repo %}<a href="{{ project.repo }}" target="_blank" class="btn-pill btn-git">Code</a>{% endif %}
{% if project.website %}<a href="{{ project.website }}" target="_blank" class="btn-pill btn-website">Website</a>{% endif %}
{% if project.docs %}<a href="{{ project.docs }}" target="_blank" class="btn-pill btn-link">Docs</a>{% endif %}
{% if project.paper %}<a href="{{ project.paper }}" target="_blank" class="btn-pill btn-link">Paper</a>{% endif %}
</div>
{% endif %}
{% if project.language or project.license or project.role %}
<p style="color: var(--text-secondary); font-size: 0.875rem;">
{% if project.language %}{{ project.language }}{% endif %}
{% if project.license %} &middot; {{ project.license }}{% endif %}
{% if project.role %} &middot; {{ project.role }}{% endif %}
</p>
{% endif %}
{{ project.description | markdownify }}
</div>
{% endfor %}

{% unless site.data.projects.size > 0 %}
<p class="text-muted">No projects listed yet. Add entries to <code>_data/projects.yml</code>.</p>
{% endunless %}
