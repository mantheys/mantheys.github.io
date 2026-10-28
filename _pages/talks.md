---
title: "Talks"
layout: page
permalink: /talks/
---

# Talks & Posters

{% assign groups = "conferences,schools" | split: "," %}
{% for g in groups %}
{% assign items = site.data.talks | where: "section", g %}
{% if items.size > 0 %}
<h2>{{ g | capitalize }}</h2>
<div class="section-card">
<ul>
{% for t in items %}
<li>
<strong>{{ t.title }}</strong> — <em>{{ t.kind }}</em><br>
{{ t.event }}{% if t.location %}, {{ t.location }}{% endif %} ({{ t.date }} {{ t.year }})
{% if t.url %} &middot; <a href="{{ t.url }}">link</a>{% endif %}
{% if t.slides %} &middot; <a href="{{ t.slides }}">slides</a>{% endif %}
</li>
{% endfor %}
</ul>
</div>
{% endif %}
{% endfor %}
