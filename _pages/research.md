---
title: "Research"
layout: page
permalink: /research/
math: true
---

# {% include t.html key="research" %}

{% assign default_lang = site.data.i18n.languages.first.code %}
{% for r in site.data.research %}
<div class="section-card">
<h2>{{ r.title }}</h2>
<p style="color: var(--text-secondary); font-style: italic;">{% include tf.html obj=r field="label" %} &middot; {% include tx.html text=r.location %} &middot; {{ r.dates }}</p>
{% for l in site.data.i18n.languages %}
{% capture key %}paragraphs_{{ l.code }}{% endcapture %}
{% assign paras = r[key] | default: r.paragraphs %}
<div data-l="{{ l.code }}" lang="{{ l.code }}" markdown="0">
{% for para in paras %}
{{ para | markdownify }}
{% endfor %}
</div>
{% endfor %}
</div>
{% endfor %}
