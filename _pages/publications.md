---
title: "Publications"
layout: page
permalink: /publications/
---

# Publications

Generated from my [INSPIRE-HEP record]({{ site.links.inspire }}) by
`tools/fetch_inspire.py` and refreshed weekly.

<input type="text" class="pub-search" id="pubSearch" placeholder="Filter by title, author, or year...">

<div class="section-card" id="pubList">
<h2>Preprints</h2>

{% bibliography --query @unpublished %}

<h2>Journal Articles</h2>

{% bibliography --query @article %}

<h2>Conference Proceedings</h2>

{% bibliography --query @inproceedings %}
</div>
