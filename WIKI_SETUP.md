---
created: 2026-01-11 23:00:24 +0900
updated: 2026-01-11 23:08:18 +0900
---
# Wiki Setup Guide

John Grib 스타일의 위키 기능이 추가된 Jekyll 블로그입니다.

## 📁 디렉토리 구조

```
junseokyoon.github.io/
├── .github/
│   └── workflows/
│       └── wiki-build.yml          # GitHub Actions 설정
├── _config.yml                     # Jekyll 설정 (위키 컬렉션 추가)
├── _layouts/
│   └── wiki.html                   # 위키 레이아웃
├── _wiki/                          # 위키 문서들
│   ├── index.md                    # 위키 홈페이지
│   ├── jekyll.md                   # 샘플 문서
│   ├── github-pages.md             # 샘플 문서
│   └── markdown.md                 # 샘플 문서
└── scripts/                        # Python 스크립트들
    ├── process_wikilinks.py        # [[링크]] 변환
    ├── generate_backlinks.py       # 백링크 생성
    └── generate_index.py           # 인덱스 생성 (선택)
```

## 🚀 설치 방법

### 1. 파일 추가

다운로드한 파일들을 저장소에 추가:

```
_config.yml          → 기존 파일에 위키 설정 추가
_layouts/wiki.html   → 새 파일 추가
_wiki/index.md       → 새 파일 추가
_wiki/*.md           → 샘플 문서들 (선택)
.github/workflows/wiki-build.yml → 새 파일 추가
scripts/*.py         → 새 파일 추가
```

### 2. GitHub Pages 설정

1. GitHub 저장소 → Settings → Pages
2. Source: "GitHub Actions" 선택
3. 저장

### 3. 첫 Push

```bash
git add .
git commit -m "Add wiki functionality"
git push
```

GitHub Actions가 자동으로 빌드를 시작합니다!

## ✍️ 위키 문서 작성법

### 새 문서 만들기

`_wiki/` 폴더에 마크다운 파일 생성:

```markdown
---
layout: wiki
title: "문서 제목"
date: 2025-01-11
tags: [태그1, 태그2]
---

# 문서 제목

내용을 여기에 작성합니다.

## 위키 링크 사용

다른 문서를 참조하려면 [[문서이름]] 형식으로 작성하세요.
예: [[Jekyll]], [[GitHub Pages]]

GitHub Actions가 자동으로 이를 실제 링크로 변환합니다!
```

### Front Matter 설명

- `layout: wiki` - 필수 (위키 레이아웃 사용)
- `title` - 문서 제목
- `date` - 작성일 (YYYY-MM-DD)
- `updated` - 수정일 (선택)
- `tags` - 태그 배열 (선택)
- `parent` - 상위 문서 (선택)

## 🔗 위키 링크 사용법

### 기본 문법

```markdown
[[문서이름]]
```

### 예시

```markdown
# Jekyll 소개

[[Jekyll]]은 정적 사이트 생성기입니다.
[[GitHub Pages]]에서 무료로 호스팅할 수 있습니다.

자세한 내용은 [[Jekyll 설치 가이드]]를 참조하세요.
```

### 자동 변환

GitHub Actions가 다음과 같이 변환합니다:

```markdown
[Jekyll](/wiki/jekyll/)
[GitHub Pages](/wiki/github-pages/)
[Jekyll 설치 가이드](/wiki/jekyll-install-guide/)
```

## 🔄 작동 원리

```
1. iPad/Mac에서 [[wikilink]] 형식으로 글 작성
   ↓
2. Working Copy에서 commit & push
   ↓
3. GitHub Actions 자동 실행:
   - process_wikilinks.py → [[링크]] 변환
   - generate_backlinks.py → 백링크 추가
   - Jekyll 빌드
   ↓
4. GitHub Pages 자동 배포
   ↓
5. https://junseokyoon.github.io/wiki/ 에서 확인
```

## 📱 iPad에서 작업하기

### Working Copy 사용

1. Working Copy에서 저장소 열기
2. `_wiki/new-document.md` 파일 생성
3. 내용 작성 ([[wikilink]] 사용)
4. Commit & Push
5. 자동 빌드 완료까지 1-2분 대기

### Drafts + Working Copy

1. Drafts에서 글 작성
2. Working Copy 액션으로 전송
3. 자동 배포

## 🛠️ 로컬 테스트 (선택)

Mac에서 로컬 테스트:

```bash
# 스크립트 실행
python scripts/process_wikilinks.py
python scripts/generate_backlinks.py

# Jekyll 서버 실행
bundle exec jekyll serve

# http://localhost:4000/wiki/ 에서 확인

# 테스트 후 원본 복원
git checkout _wiki/
```

## 🎯 주요 기능

### 1. 위키 링크
- `[[문서이름]]` 형식으로 간편하게 링크
- 자동으로 URL 변환

### 2. 백링크
- 각 문서 하단에 "이 문서를 참조하는 문서들" 자동 생성
- 문서 간 관계를 쉽게 파악

### 3. 태그 시스템
- 태그별로 문서 분류
- 위키 홈에서 태그별 필터링

### 4. 자동 인덱스
- 전체 문서 목록
- 최근 수정 문서
- 태그별 문서

## 🔍 트러블슈팅

### Actions 실패 시

1. GitHub → Actions 탭 확인
2. 실패한 workflow 클릭
3. 로그 확인
4. 주요 오류:
   - 파일 인코딩 문제 → UTF-8로 저장
   - 문법 오류 → Front matter 확인
   - 링크 오류 → 대상 파일 존재 확인

### 링크가 변환되지 않을 때

- 대상 파일이 `_wiki/` 폴더에 있는지 확인
- 파일명과 [[링크]] 텍스트가 일치하는지 확인
- 대소문자 구분 없음 (자동 처리)

### 백링크가 안 보일 때

- Actions가 성공적으로 실행되었는지 확인
- 최소 1개 이상의 다른 문서가 해당 문서를 링크하는지 확인

## 📚 샘플 문서

3개의 샘플 문서가 포함되어 있습니다:

- `jekyll.md` - Jekyll 소개
- `github-pages.md` - GitHub Pages 설명
- `markdown.md` - Markdown 문법

이 문서들을 참고하거나 삭제하고 새로 작성하세요.

## 🎨 커스터마이징

### 레이아웃 수정

`_layouts/wiki.html` 파일에서:
- 스타일 변경
- 메타데이터 표시 형식
- 네비게이션 구조

### 스크립트 수정

`scripts/` 폴더의 Python 스크립트:
- 링크 변환 규칙 수정
- 백링크 표시 형식 변경
- 추가 자동화 기능

## 🚦 다음 단계

1. ✅ 샘플 문서 확인
2. ✅ 첫 문서 작성
3. ✅ 위키 링크로 문서 연결
4. ✅ 태그 추가
5. ✅ 백링크 확인

---

**문제가 있나요?**
- GitHub Issues에 질문 남기기
- Actions 로그 확인하기
- 샘플 문서 참고하기
