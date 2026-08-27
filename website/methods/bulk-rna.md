---
layout: default
title: Bulk RNA
parent: Methods
nav_order: 2
---

{% assign family = site.data.methods.bulk_rna %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} canonical notebooks · source links below</p>

<div class="notebook-grid">
{% for notebook in family.notebooks %}
  {% include notebook-card.html notebook=notebook %}
{% endfor %}
</div>
