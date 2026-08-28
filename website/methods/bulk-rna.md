---
layout: default
title: Bulk RNA
parent: Methods
nav_order: 2
search_family: bulk_rna
---

{% assign family = site.data.methods.bulk_rna %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} notebooks · view or download the QMD files below</p>

<div class="notebook-grid">
{% for notebook in family.notebooks %}
  {% include notebook-card.html notebook=notebook %}
{% endfor %}
</div>
