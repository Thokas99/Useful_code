---
layout: default
title: Multiome
parent: Methods
nav_order: 4
search_family: multiome
---

{% assign family = site.data.methods.multiome %}
<p class="page-intro">{{ family.description }}</p>
<p class="catalog-meta">{{ family.notebooks.size }} notebooks · view or download the QMD files below</p>
{% include section-download.html family=family %}

<div class="notebook-grid">
{% for notebook in family.notebooks %}
{% include notebook-card.html notebook=notebook family=family %}
{% endfor %}
</div>
