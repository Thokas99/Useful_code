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

## Other resources

Browse [Examples]({{ site.baseurl }}/examples/), [Cheatsheets]({{ site.baseurl }}/cheatsheets/), and [Miscellaneous]({{ site.baseurl }}/miscellaneous/) for project provenance and reusable reporting material.
