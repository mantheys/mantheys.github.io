---
title: "Talks"
layout: page
permalink: /talks/
---

# {% include t.html key="talks" %}

{% assign groups = "conferences,schools" | split: "," %}
{% for g in groups %}
{% assign items = site.data.talks | where: "section", g %}
{% if items.size > 0 %}
<h2>{% include t.html key=g %}</h2>
<div class="section-card">
<ul>
{% for t in items %}
<li>
<strong>{{ t.title }}</strong> — <em>{% include t.html key=t.kind %}</em><br>
{{ t.event }}{% if t.location %}, {% include tx.html text=t.location %}{% endif %} ({% capture when %}{{ t.date }} {{ t.year }}{% endcapture %}{% include tx.html text=when %})
{% if t.url %} &middot; <a href="{{ t.url }}">{% include t.html key="link" %}</a>{% endif %}
{% if t.slides %} &middot; <a href="{{ t.slides }}">{% include t.html key="slides" %}</a>{% endif %}
</li>
{% endfor %}
</ul>
</div>
{% endif %}
{% endfor %}
