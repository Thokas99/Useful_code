---
layout: default
title: Multiome
parent: Methods
nav_order: 4
---

{% assign family = site.data.methods.multiome %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} canonical notebooks · source links below</p>

<div class="notebook-grid">
{% for notebook in family.notebooks %}
  {% include notebook-card.html notebook=notebook %}
{% endfor %}
</div>
