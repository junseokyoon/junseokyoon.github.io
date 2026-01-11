#!/usr/bin/env python3
"""
Index Generator (Optional)
태그별 인덱스 페이지를 자동으로 생성합니다.
"""

import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List
from datetime import datetime

class IndexGenerator:
    def __init__(self, wiki_dir: str = "_wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.pages_by_tag: Dict[str, List[dict]] = defaultdict(list)
        self.all_pages: List[dict] = []
    
    def _extract_front_matter(self, content: str) -> dict:
        """front matter 파싱"""
        if not content.startswith('---'):
            return {}
        
        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}
            
            front_matter = parts[1]
            metadata = {}
            
            # title 추출
            title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', 
                                   front_matter, re.MULTILINE)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            # tags 추출
            tags_match = re.search(r'^tags:\s*\[(.+?)\]', front_matter, re.MULTILINE)
            if tags_match:
                tags_str = tags_match.group(1)
                metadata['tags'] = [t.strip().strip('"\'') for t in tags_str.split(',')]
            
            # date 추출
            date_match = re.search(r'^date:\s*(.+?)$', front_matter, re.MULTILINE)
            if date_match:
                metadata['date'] = date_match.group(1).strip()
            
            # updated 추출
            updated_match = re.search(r'^updated:\s*(.+?)$', front_matter, re.MULTILINE)
            if updated_match:
                metadata['updated'] = updated_match.group(1).strip()
            
            return metadata
            
        except Exception as e:
            print(f"⚠️  Error parsing front matter: {e}")
            return {}
    
    def _get_url_path(self, file_path: Path) -> str:
        """파일 경로를 URL로 변환"""
        relative_path = file_path.relative_to(self.wiki_dir)
        url_path = str(relative_path.with_suffix('')).replace('\\', '/')
        return f"/wiki/{url_path}/"
    
    def collect_pages(self):
        """모든 위키 페이지 정보 수집"""
        if not self.wiki_dir.exists():
            print(f"⚠️  {self.wiki_dir} directory not found")
            return
        
        print("📚 Collecting wiki pages...")
        
        for md_file in self.wiki_dir.rglob("*.md"):
            if md_file.name == "index.md" or md_file.stem.startswith("tag-"):
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
                metadata = self._extract_front_matter(content)
                
                page_info = {
                    'file': md_file,
                    'title': metadata.get('title', md_file.stem.replace('-', ' ').title()),
                    'url': self._get_url_path(md_file),
                    'tags': metadata.get('tags', []),
                    'date': metadata.get('date', ''),
                    'updated': metadata.get('updated', '')
                }
                
                self.all_pages.append(page_info)
                
                # 태그별로 분류
                for tag in page_info['tags']:
                    self.pages_by_tag[tag].append(page_info)
                
            except Exception as e:
                print(f"❌ Error processing {md_file}: {e}")
        
        print(f"✅ Collected {len(self.all_pages)} pages")
        print(f"🏷️  Found {len(self.pages_by_tag)} unique tags")
    
    def generate_tag_pages(self):
        """태그별 인덱스 페이지 생성"""
        if not self.pages_by_tag:
            print("ℹ️  No tags found, skipping tag page generation")
            return
        
        print("🏷️  Generating tag pages...")
        print("-" * 50)
        
        for tag, pages in self.pages_by_tag.items():
            tag_file = self.wiki_dir / f"tag-{tag}.md"
            
            # 페이지를 제목순으로 정렬
            sorted_pages = sorted(pages, key=lambda x: x['title'])
            
            # 태그 페이지 내용 생성
            content = f"""---
layout: default
title: "태그: {tag}"
permalink: /wiki/tag-{tag}/
---

# 태그: {tag}

총 {len(pages)}개의 문서

"""
            
            for page in sorted_pages:
                content += f"- [{page['title']}]({page['url']})\n"
                if page['date']:
                    content += f"  - 작성: {page['date']}\n"
            
            content += "\n---\n\n[← 위키 홈](/wiki/)\n"
            
            try:
                tag_file.write_text(content, encoding='utf-8')
                print(f"✅ Created: {tag_file.name} ({len(pages)} pages)")
            except Exception as e:
                print(f"❌ Error creating {tag_file}: {e}")
        
        print("-" * 50)
    
    def generate_all_pages_index(self):
        """전체 페이지 인덱스 생성 (선택사항)"""
        if not self.all_pages:
            return
        
        index_file = self.wiki_dir / "all-pages.md"
        
        # 제목순 정렬
        sorted_pages = sorted(self.all_pages, key=lambda x: x['title'])
        
        content = f"""---
layout: default
title: "전체 문서"
permalink: /wiki/all-pages/
---

# 전체 문서

총 {len(self.all_pages)}개의 문서

"""
        
        # 알파벳/한글 첫 글자별로 그룹화
        current_letter = None
        for page in sorted_pages:
            first_char = page['title'][0].upper()
            
            if first_char != current_letter:
                current_letter = first_char
                content += f"\n## {current_letter}\n\n"
            
            content += f"- [{page['title']}]({page['url']})"
            
            if page['tags']:
                tags_str = ', '.join([f'#{tag}' for tag in page['tags']])
                content += f" - {tags_str}"
            
            content += "\n"
        
        content += "\n---\n\n[← 위키 홈](/wiki/)\n"
        
        try:
            index_file.write_text(content, encoding='utf-8')
            print(f"✅ Created: {index_file.name}")
        except Exception as e:
            print(f"❌ Error creating {index_file}: {e}")
    
    def generate_all(self):
        """모든 인덱스 생성"""
        self.collect_pages()
        self.generate_tag_pages()
        self.generate_all_pages_index()
        
        print("✨ Index generation complete")

def main():
    print("=" * 50)
    print("Index Generator (Optional)")
    print("=" * 50)
    
    generator = IndexGenerator()
    generator.generate_all()
    
    print("=" * 50)

if __name__ == "__main__":
    main()
