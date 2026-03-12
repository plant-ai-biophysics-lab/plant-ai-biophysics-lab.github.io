---
layout: single
permalink: /
title: "Papers"
classes: wide
---

{% assign pubs = site.data.publications | sort: "year" | reverse %}
{% if pubs and pubs.size > 0 %}
<ul class="publications-list" style="padding-left: 0;">
  {% for pub in pubs %}
    {% include publication_item.html pub=pub %}
  {% endfor %}
</ul>
{% else %}
*Publications are populated from OpenAlex (J. Mason Earles, Mason Earles, UC Davis). Add entries or `podcast_url` / `podcast_drive_id` in `_data/publications.yml` to customize.*
{% endif %}
