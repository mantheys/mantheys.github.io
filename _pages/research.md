---
title: "Research"
layout: page
permalink: /research/
math: true
---

# {% include t.html key="research" %}

<div class="research-tabs" data-tabs markdown="0">
<div class="tab-list" role="tablist">
<a href="#overview" class="tab-link" role="tab" data-tab="overview">{% include t.html key="chip_overview" %}</a>
{% for t in site.data.research_topics %}<a href="#{{ t.id }}" class="tab-link" role="tab" data-tab="{{ t.id }}">{% for l in site.data.i18n.languages %}<span data-l="{{ l.code }}" lang="{{ l.code }}">{{ t.title[l.code] | default: t.title.en }}</span>{% endfor %}</a>
{% endfor %}</div>

<div class="tab-panel" id="overview" role="tabpanel" markdown="0">
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
</div>

{% for t in site.data.research_topics %}
<div class="tab-panel" id="{{ t.id }}" role="tabpanel" markdown="0">
<div class="section-card">
<h2>{% for l in site.data.i18n.languages %}<span data-l="{{ l.code }}" lang="{{ l.code }}">{{ t.title[l.code] | default: t.title.en }}</span>{% endfor %}</h2>
{% for l in site.data.i18n.languages %}
{% assign paras = t.body[l.code] | default: t.body.en %}
<div data-l="{{ l.code }}" lang="{{ l.code }}" markdown="0">
{% for para in paras %}
{{ para | markdownify }}
{% endfor %}
</div>
{% endfor %}
</div>
</div>
{% endfor %}
</div>
