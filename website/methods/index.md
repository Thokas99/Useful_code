---
layout: default
title: Methods
nav_order: 2
has_children: true
has_toc: false
---

This is the catalog of the active reusable library. Canonical templates live
in the repository under `templates/`; this site only describes and links to
them. It does not execute QMD files, install scientific environments, or build
rendered notebook copies.

<div class="catalog-grid">
  {% assign family = site.data.methods.single_cell %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.bulk_rna %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.scatac %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.multiome %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.mofa %}{% include family-card.html family=family %}
  {% assign family = site.data.methods.biomarker_ml %}{% include family-card.html family=family %}
</div>
