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
    {% case key %}
      {% when "single_cell" %}{% assign family = site.data.methods.single_cell %}
      {% when "bulk_rna" %}{% assign family = site.data.methods.bulk_rna %}
      {% when "scatac" %}{% assign family = site.data.methods.scatac %}
      {% when "multiome" %}{% assign family = site.data.methods.multiome %}
      {% when "mofa" %}{% assign family = site.data.methods.mofa %}
      {% when "biomarker_ml" %}{% assign family = site.data.methods.biomarker_ml %}
    {% endcase %}
    {% include family-card.html family=family %}
  {% endfor %}
</div>
