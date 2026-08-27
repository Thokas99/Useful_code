---
layout: default
title: Useful code
nav_order: 1
has_toc: false
---

Reusable bioinformatics workflows derived from real analytical projects.

This site is a small catalog. The executable source of truth remains in the
canonical notebooks on [GitHub](https://github.com/Thokas99/Useful_code/tree/main/templates).
Notebooks are not executed or rendered into this site.

[Browse methods]({{ site.baseurl }}/methods/){: .btn .btn-primary }
[View repository](https://github.com/Thokas99/Useful_code){: .btn}

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
