---
layout: wikiindex
title: wiki
toc: true
public: true
parent:
comment: false
updated: 2026-01-13 00:42:14 +0900
regenerate: true
created: 2026-01-05 00:00:48 +0900
---

## [[how-to]]

* [[mathjax-latex]]


---

## blog posts
<div>
    <ul>
{% for post in site.posts %}
    {% if post.public == true %}
        <li>
            <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">
                {{ post.title }}
            </a>
        </li>
    {% endif %}
{% endfor %}
    </ul>
</div>

