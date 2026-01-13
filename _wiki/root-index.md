---
layout: wiki
title: wiki
toc: true
public: true
parent:
comment: false
updated: 2026-01-14 00:07:51 +0900
created: 2026-01-05 00:00:48 +0900
---
* TOC 
{:toc}

## 링크 구조 확인
* [[how-to]]
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

