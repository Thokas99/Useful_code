---
layout: default
title: scATAC
parent: Methods
nav_order: 3
search_family: scatac
---

{% assign family = site.data.methods.scatac %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} canonical notebooks · source links below</p>

<div class="notebook-grid">
{% for notebook in family.notebooks %}
  {% include notebook-card.html notebook=notebook %}
{% endfor %}
</div>
