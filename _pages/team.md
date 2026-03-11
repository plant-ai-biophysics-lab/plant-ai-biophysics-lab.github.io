---
layout: single
permalink: /team/
title: "Team"
---

{% assign sorted = site.data.team.members | sort: "name" %}
{% for member in sorted %}
{% include team_member.html member=member %}
{% endfor %}
