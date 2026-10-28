---
title: "Home"
layout: homelay
permalink: /
---

<h1 class="home-hero">{{ site.name }}</h1>
<p class="home-hero-sub">{{ site.title }} &middot; {{ site.institution }}</p>

<div class="chip-container" markdown="0">
<a href="{{ '/research' | relative_url }}" class="chip">Neutrino Oscillations</a>
<a href="{{ '/research' | relative_url }}" class="chip">Solar Neutrinos</a>
<a href="{{ '/research' | relative_url }}" class="chip">Liquid Argon TPCs</a>
<a href="{{ '/research' | relative_url }}" class="chip">Photon Detection</a>
<a href="{{ '/research' | relative_url }}" class="chip">X-ARAPUCA</a>
<a href="{{ '/research' | relative_url }}" class="chip">DUNE</a>
</div>

I work on low-energy neutrino physics for the **Deep Underground Neutrino Experiment**
(DUNE), spanning detector hardware and physics analysis. My work covers cryogenic
characterisation of **X-ARAPUCA** photon detectors, Monte Carlo simulation and
reconstruction of low-energy charge and scintillation signals in LArSoft, and
sensitivity studies for **solar neutrinos** — the day–night asymmetry, HEP neutrino
discovery potential, and DUNE's reach on the solar oscillation parameters.

<div class="callout callout-success" markdown="0">
<div class="callout-title">{% include icon.html name="cv" class="callout-icon" %} Curriculum Vitae</div>
<p>My CV is generated from the same data as this site and rebuilt on every commit.
<a href="{{ '/assets/cv.pdf' | relative_url }}">Download the PDF &rarr;</a></p>
</div>

{% capture selected %}{% bibliography --query @*[selected=true] %}{% endcapture %}
{% if selected contains "pub-entry" %}
## Selected publications

<div class="section-card selected-pubs" markdown="0">
{{ selected }}
<p style="margin: var(--space-4) 0 0;"><a href="{{ '/publications' | relative_url }}">All publications &rarr;</a></p>
</div>
{% endif %}
