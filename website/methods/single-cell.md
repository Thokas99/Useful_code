---
layout: default
title: Single-cell
parent: Methods
nav_order: 1
search_family: single_cell
---

{% assign family = site.data.methods.single_cell %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} notebooks · view or download the QMD files below</p>
{% include section-download.html family=family %}

<div class="notebook-grid">
{% for notebook in family.notebooks %}
{% include notebook-card.html notebook=notebook family=family %}
{% endfor %}
</div>
