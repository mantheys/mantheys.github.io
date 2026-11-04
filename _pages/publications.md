---
title: "Publications"
layout: page
permalink: /publications/
---

# {% include t.html key="publications" %}

<div markdown="0">{% include t.html key="pubs_intro" md=true sub="__URL__" with=site.links.inspire %}</div>

<input type="text" class="pub-search" id="pubSearch" {% include ta.html attr="placeholder" key="pubs_filter" %}>

<div class="section-card" id="pubList">
<h2>{% include t.html key="preprints" %}</h2>

{% bibliography --query @unpublished %}

<h2>{% include t.html key="articles" %}</h2>

{% bibliography --query @article %}

<h2>{% include t.html key="proceedings" %}</h2>

{% bibliography --query @inproceedings %}
</div>
