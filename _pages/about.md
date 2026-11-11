---
title: "About"
layout: page
permalink: /about/
---

# {% include t.html key="about" %}

<div class="section-card">
<div class="pi-card">
<div>
<h2 class="pi-name">{{ site.name }}</h2>
<p style="font-style: italic; color: var(--text-secondary);">{% include t.html key="site_title" %}, {{ site.institution }}</p>
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
<h3>{% include t.html key="education" %}</h3>
<ul>
{% for e in site.data.education %}
<li><strong>{% include tf.html obj=e field="degree" %}</strong>, {{ e.institution }}, {% include tx.html text=e.location %} ({{ e.dates }}{% if e.graduated %}, {% include t.html key="graduated" %} {% include tx.html text=e.graduated %}{% endif %}{% if e.status %}, {% include tf.html obj=e field="status" %}{% endif %})<br>
<span style="color: var(--text-secondary);">{% include t.html key="thesis" %}: {{ e.thesis }}</span></li>
{% endfor %}
</ul>
</div>

<div class="section-card">
<h3>{% include t.html key="positions" %}</h3>
<ul>
{% for p in site.data.experience.positions %}
<li><strong>{% include tf.html obj=p field="title" %}</strong>, {{ p.organization }}, {% include tx.html text=p.location %} ({% include tx.html text=p.dates %})</li>
{% endfor %}
</ul>
</div>

<div class="section-card">
<h3>{% include t.html key="languages" %}</h3>
<ul>
{% for l in site.data.skills.languages %}
<li><strong>{% include tf.html obj=l field="name" %}</strong> — {% include tf.html obj=l field="level" %}</li>
{% endfor %}
</ul>
</div>
