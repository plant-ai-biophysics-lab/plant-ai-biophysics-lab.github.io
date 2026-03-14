---
layout: single
permalink: /team/
title: "Team"
---

## Current Members

{% assign current = site.data.team.members | sort: "name" %}
{% for member in current %}
{% include team_member.html member=member %}
{% endfor %}

{% if site.data.team.past_members and site.data.team.past_members.size > 0 %}
## Past Members

{% assign alumni = site.data.team.past_members | sort: "name" %}
{% for member in alumni %}
{% include team_member.html member=member %}
{% endfor %}
{% endif %}
