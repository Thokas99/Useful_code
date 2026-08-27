---
layout: default
title: Single-cell
parent: Methods
nav_order: 1
---

{% assign family = site.data.methods.single_cell %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} canonical notebooks · source links below</p>

<div class="notebook-grid">
{% for notebook in family.notebooks %}
  {% include notebook-card.html notebook=notebook %}
{% endfor %}
</div>
