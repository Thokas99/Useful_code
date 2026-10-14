---
layout: default
title: Useful code
nav_order: 1
has_toc: false
---

<section class="hero-panel">
  <p class="hero-kicker">PERSONAL RESEARCH COOKBOOK</p>
  <h2>Readable workflows for bioinformatics.</h2>
  <p>Browse R, Python, and Quarto guides by method. Open a notebook on GitHub to inspect its code and assumptions.</p>
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
  <div class="stat"><strong class="stat-value">{{ canonical_notebook_count }}</strong><span>notebooks</span></div>
  <div class="stat"><strong class="stat-value">6</strong><span>method areas</span></div>
</div>

<p class="site-caution"><strong>Research workflows.</strong> Check assumptions and validate outputs for your study. <a href="{{ site.baseurl }}/about/">Read the reuse guidance.</a></p>
<p class="search-note">Search includes notebook text.</p>

## Browse the library

<div class="catalog-grid">
  {% assign family = site.data.methods.single_cell %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.bulk_rna %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.scatac %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.multiome %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.mofa %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.biomarker_ml %}{% include family-card.html family=family %}
</div>

## More resources

Browse [project examples]({{ site.baseurl }}/examples/) and
[reporting resources]({{ site.baseurl }}/miscellaneous/).
