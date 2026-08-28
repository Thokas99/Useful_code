---
layout: default
title: Multi-omics / MOFA
parent: Methods
nav_order: 5
search_family: mofa
---

{% assign family = site.data.methods.mofa %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} notebooks · view or download the QMD files below</p>
{% include section-download.html family=family %}

<div class="notebook-grid">
{% for notebook in family.notebooks %}
{% include notebook-card.html notebook=notebook family=family %}
{% endfor %}
</div>
