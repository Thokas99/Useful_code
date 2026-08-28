---
layout: default
title: Useful code
nav_order: 1
has_toc: false
---

<section class="hero-panel">
  <p class="hero-kicker">PERSONAL RESEARCH COOKBOOK</p>
  <h2>Readable workflows for real analytical work.</h2>
  <p>Explore reusable R, Python, and Quarto methods, inspect their assumptions, and open the canonical notebook when you are ready to adapt it.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{{ site.baseurl }}/methods/">Browse methods</a>
    <a class="btn" href="https://github.com/Thokas99/Useful_code">View repository</a>
  </div>
</section>

{% assign canonical_notebook_count = site.data.methods.single_cell.notebooks.size
  | plus: site.data.methods.bulk_rna.notebooks.size
  | plus: site.data.methods.scatac.notebooks.size
  | plus: site.data.methods.multiome.notebooks.size
  | plus: site.data.methods.mofa.notebooks.size
  | plus: site.data.methods.biomarker_ml.notebooks.size %}
<div class="stat-grid" aria-label="Catalog summary">
  <div class="stat"><strong class="stat-value">{{ canonical_notebook_count }}</strong><span>canonical notebooks</span></div>
  <div class="stat"><strong class="stat-value">6</strong><span>method families</span></div>
  <div class="stat"><strong class="stat-value">1</strong><span>GitHub source of truth</span></div>
</div>

<p class="site-caution"><strong>Personal research scripts.</strong> Review assumptions and validate independently before reuse. <a href="{{ site.baseurl }}/about/">Read the full disclaimer.</a></p>

The site is a small catalog. The canonical notebooks on
[GitHub](https://github.com/Thokas99/Useful_code/tree/main/templates) remain the
source of truth; notebooks are not executed or rendered into this site.

<p class="search-note"><strong>Search inside the notebooks.</strong> The site search also indexes the full source text of every canonical QMD, while results still lead to the family catalog and the original GitHub file.</p>

## Browse the library

<div class="catalog-grid">
  {% assign family = site.data.methods.single_cell %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.bulk_rna %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.scatac %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.multiome %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.mofa %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.biomarker_ml %}{% include family-card.html family=family %}
</div>

## Other resources

Browse [Examples]({{ site.baseurl }}/examples/), [Cheatsheets]({{ site.baseurl }}/cheatsheets/), and [Miscellaneous]({{ site.baseurl }}/miscellaneous/) for project provenance and reusable reporting material.
