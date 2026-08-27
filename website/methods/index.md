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
  {% for key in "single_cell,bulk_rna,scatac,multiome,mofa,biomarker_ml" | split: "," %}
    {% assign family = site.data.methods[key] %}
    {% include family-card.html family=family %}
  {% endfor %}
</div>
