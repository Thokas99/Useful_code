---
layout: default
title: Multi-omics / MOFA
parent: Methods
nav_order: 5
---

{% assign family = site.data.methods.mofa %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} canonical notebooks · source links below</p>

<div class="notebook-grid">
{% for notebook in family.notebooks %}
  {% include notebook-card.html notebook=notebook %}
{% endfor %}
</div>
