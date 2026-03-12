---
layout: single
permalink: /
title: ""
author_profile: false
sidebar:
  - nav: single_page_nav
  - text: "AI for Plant-based Agriculture and Food Systems"
classes: wide page--no-top-space
---

<h2 id="papers">Papers</h2>

{% assign pubs = site.data.publications | sort: "year" | reverse %}
{% if pubs and pubs.size > 0 %}
<ul class="publications-list" style="padding-left: 0;">
  {% for pub in pubs %}
    {% include publication_item.html pub=pub %}
  {% endfor %}
</ul>
{% else %}
*Publications are populated from OpenAlex. Add entries or `podcast_url` / `podcast_drive_id` in `_data/publications.yml` to customize.*
{% endif %}

<h2 id="team">Team</h2>

<div class="team-grid">
{% assign sorted = site.data.team.members | sort: "name" %}
{% for member in sorted %}
{% include team_member.html member=member %}
{% endfor %}
</div>

<h2 id="section-code">Code</h2>

- **[Lab](https://github.com/plant-ai-biophysics-lab)** — UC Davis research lab focused on developing AI-enabled solutions for agriculture and food systems.
- **[GEMINI](https://github.com/GEMINI-Breeding)** — G×E×M Innovation in Intelligence for Climate Adaptation: a state-of-the-art breeding toolkit combining AI-enabled sensing, 3-D crop modeling, and molecular breeding to accelerate stress-resistant, nutritious staple crops for low and middle-income countries. [Docs](https://gemini-breeding.github.io/)
- **[AgML](https://github.com/Project-AgML/AgML)** — A centralized framework for agricultural machine learning. Provides access to public agricultural datasets for common deep learning tasks, with standard benchmarks, pretrained models, and synthetic data generation.
