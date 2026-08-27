---
layout: default
title: Useful code
nav_order: 1
has_toc: false
---

<section class="hero-panel">
  <p class="hero-kicker">BIOINFORMATICS · R · PYTHON · QUARTO</p>
  <h2>Readable workflows for real analytical work.</h2>
  <p>Explore reusable methods, inspect their assumptions, and open the canonical notebook when you are ready to adapt it.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{{ site.baseurl }}/methods/">Browse methods</a>
    <a class="btn" href="https://github.com/Thokas99/Useful_code">View repository</a>
  </div>
</section>

<div class="stat-grid" aria-label="Catalog summary">
  <div class="stat"><strong class="stat-value">37</strong><span>canonical notebooks</span></div>
  <div class="stat"><strong class="stat-value">6</strong><span>method families</span></div>
  <div class="stat"><strong class="stat-value">1</strong><span>GitHub source of truth</span></div>
</div>

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
