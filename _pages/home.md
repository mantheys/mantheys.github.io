---
title: "Home"
layout: homelay
permalink: /
---

<h1 class="home-hero">{{ site.name }}</h1>
<p class="home-hero-sub">{% include t.html key="site_title" %} &middot; {{ site.institution }}</p>

<div class="chip-container" markdown="0">
<a href="{{ '/research/' | relative_url }}#oscillations" class="chip">{% include t.html key="chip_oscillations" %}</a>
<a href="{{ '/research/' | relative_url }}#solar" class="chip">{% include t.html key="chip_solar" %}</a>
<a href="{{ '/research/' | relative_url }}#lartpc" class="chip">{% include t.html key="chip_lartpc" %}</a>
<a href="{{ '/research/' | relative_url }}#photon-detection" class="chip">{% include t.html key="chip_pds" %}</a>
<a href="{{ '/research/' | relative_url }}#overview" class="chip">DUNE</a>
</div>

<div markdown="0">{% capture research_url %}{{ '/research/' | relative_url }}{% endcapture %}{% include t.html key="home_intro" md=true sub="@R@" with=research_url %}</div>

<div class="callout callout-success" markdown="0">
<div class="callout-title">{% include icon.html name="cv" class="callout-icon" %} {% include t.html key="cv" %}</div>
<p>{% include t.html key="cv_callout" %}
<a href="{{ '/assets/cv.pdf' | relative_url }}">{% include t.html key="cv_download" %} &rarr;</a></p>
</div>

{% comment %}
  Only papers where I am the lead author on the full INSPIRE author list.
  tools/fetch_inspire.py sets `first_author = {true}` on those BibTeX entries.
{% endcomment %}
{% capture first_author %}{% bibliography --query @*[first_author=true] %}{% endcapture %}
{% if first_author contains "pub-entry" %}
<h2 id="first-author-publications">{% include t.html key="first_author_pubs" %}</h2>

<div class="section-card selected-pubs" markdown="0">
{{ first_author }}
<p style="margin: var(--space-4) 0 0;"><a href="{{ '/publications' | relative_url }}">{% include t.html key="all_pubs" %} &rarr;</a></p>
</div>
{% endif %}
