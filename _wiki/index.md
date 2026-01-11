---
layout: default
title: Wiki
permalink: /wiki/
created: 2026-01-11 23:06:07 +0900
updated: 2026-01-11 23:06:07 +0900
---

<div class="wiki-index">
  <h1>📚 Wiki</h1>
  
  <p class="wiki-intro">
    개인 지식 저장소입니다. 문서들은 서로 연결되어 있습니다.
  </p>

  <!-- 태그별 분류 -->
  {% assign all_tags = site.wiki | map: 'tags' | join: ',' | split: ',' | uniq | sort %}
  {% if all_tags.size > 0 %}
  <section class="wiki-tags-section">
    <h2>태그로 찾기</h2>
    <div class="tag-cloud">
      {% for tag in all_tags %}
        {% if tag != "" %}
        <a href="#tag-{{ tag }}" class="tag-link">#{{ tag }}</a>
        {% endif %}
      {% endfor %}
    </div>
  </section>
  {% endif %}

  <!-- 최근 수정 문서 -->
  <section class="wiki-recent">
    <h2>최근 수정</h2>
    <ul class="wiki-list">
      {% assign sorted_wiki = site.wiki | sort: 'updated' | reverse %}
      {% for doc in sorted_wiki limit:10 %}
      <li>
        <a href="{{ doc.url }}">{{ doc.title }}</a>
        {% if doc.updated %}
        <span class="wiki-date">{{ doc.updated | date: "%Y.%m.%d" }}</span>
        {% elsif doc.date %}
        <span class="wiki-date">{{ doc.date | date: "%Y.%m.%d" }}</span>
        {% endif %}
      </li>
      {% endfor %}
    </ul>
  </section>

  <!-- 전체 문서 목록 -->
  <section class="wiki-all">
    <h2>전체 문서 ({{ site.wiki.size }}개)</h2>
    
    {% for tag in all_tags %}
      {% if tag != "" %}
      <div id="tag-{{ tag }}" class="tag-section">
        <h3>#{{ tag }}</h3>
        <ul class="wiki-list">
          {% for doc in site.wiki %}
            {% if doc.tags contains tag %}
            <li>
              <a href="{{ doc.url }}">{{ doc.title }}</a>
            </li>
            {% endif %}
          {% endfor %}
        </ul>
      </div>
      {% endif %}
    {% endfor %}

    <!-- 태그 없는 문서들 -->
    {% assign untagged = site.wiki | where_exp: "doc", "doc.tags.size == 0" %}
    {% if untagged.size > 0 %}
    <div class="tag-section">
      <h3>기타</h3>
      <ul class="wiki-list">
        {% for doc in untagged %}
        <li>
          <a href="{{ doc.url }}">{{ doc.title }}</a>
        </li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}
  </section>
</div>

<style>
.wiki-index {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.wiki-intro {
  color: #586069;
  font-size: 1.1em;
  margin-bottom: 40px;
}

.wiki-tags-section {
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e1e4e8;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.tag-link {
  padding: 5px 12px;
  background-color: #f1f8ff;
  border-radius: 15px;
  color: #0366d6;
  text-decoration: none;
  font-size: 0.9em;
  transition: all 0.2s;
}

.tag-link:hover {
  background-color: #def;
  transform: translateY(-2px);
}

.wiki-recent, .wiki-all {
  margin-bottom: 40px;
}

.wiki-recent h2, .wiki-all h2, .tag-section h3 {
  color: #24292e;
  margin-bottom: 15px;
}

.wiki-list {
  list-style: none;
  padding: 0;
}

.wiki-list li {
  margin-bottom: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #f6f8fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.wiki-list li:last-child {
  border-bottom: none;
}

.wiki-list a {
  color: #0366d6;
  text-decoration: none;
  flex-grow: 1;
}

.wiki-list a:hover {
  text-decoration: underline;
}

.wiki-date {
  color: #586069;
  font-size: 0.85em;
  margin-left: 10px;
}

.tag-section {
  margin-bottom: 30px;
}

.tag-section h3 {
  font-size: 1.2em;
  color: #0366d6;
  margin-bottom: 10px;
}

/* 다크모드 */
@media (prefers-color-scheme: dark) {
  .wiki-intro {
    color: #8b949e;
  }
  
  .wiki-tags-section {
    border-bottom-color: #30363d;
  }
  
  .tag-link {
    background-color: #161b22;
    color: #58a6ff;
  }
  
  .wiki-recent h2, .wiki-all h2, .tag-section h3 {
    color: #c9d1d9;
  }
  
  .tag-section h3 {
    color: #58a6ff;
  }
  
  .wiki-list li {
    border-bottom-color: #21262d;
  }
  
  .wiki-date {
    color: #8b949e;
  }
}
</style>
