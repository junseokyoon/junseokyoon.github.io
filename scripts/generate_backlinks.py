#!/usr/bin/env python3
"""
Backlink Generator
문서 간 링크를 분석하여 백링크를 자동으로 생성합니다.
"""

import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set

class BacklinkGenerator:
    def __init__(self, wiki_dir: str = "_wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.backlinks: Dict[str, Set[str]] = defaultdict(set)
        self.file_map: Dict[str, Path] = {}
        self.title_map: Dict[Path, str] = {}
    
    def _extract_front_matter(self, content: str) -> tuple[str, str]:
        """front matter와 본문 분리"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[1], '---' + parts[2]
        return '', content
    
    def _extract_title(self, file_path: Path) -> str:
        """파일에서 title 추출, 없으면 파일명 사용"""
        try:
            content = file_path.read_text(encoding='utf-8')
            front_matter, _ = self._extract_front_matter(content)
            
            if front_matter:
                title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', 
                                      front_matter, re.MULTILINE)
                if title_match:
                    return title_match.group(1).strip()
        except Exception as e:
            print(f"⚠️  Error reading title from {file_path}: {e}")
        
        # title이 없으면 파일명 사용
        return file_path.stem.replace('-', ' ').title()
    
    def _build_file_map(self):
        """파일명과 경로 매핑"""
        if not self.wiki_dir.exists():
            print(f"⚠️  Warning: {self.wiki_dir} directory not found")
            return
        
        for md_file in self.wiki_dir.rglob("*.md"):
            if md_file.name == "index.md":
                continue
            
            file_stem = md_file.stem.lower()
            self.file_map[file_stem] = md_file
            self.title_map[md_file] = self._extract_title(md_file)
    
    def _extract_links(self, content: str) -> List[str]:
        """마크다운 링크에서 위키 링크 추출"""
        links = []
        
        # [text](/wiki/path/) 형태의 링크 찾기
        wiki_links = re.findall(r'\[([^\]]+)\]\(/wiki/([^)]+)/?\)', content)
        for text, path in wiki_links:
            # 경로에서 파일명 추출
            link_target = Path(path).stem.lower()
            links.append(link_target)
        
        return links
    
    def analyze_links(self):
        """모든 파일의 링크 분석하여 백링크 맵 생성"""
        if not self.wiki_dir.exists():
            return
        
        print("🔗 Analyzing links...")
        
        for md_file in self.wiki_dir.rglob("*.md"):
            if md_file.name == "index.md":
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
                _, body = self._extract_front_matter(content)
                
                # 이 파일이 링크하는 대상들 찾기
                linked_targets = self._extract_links(body)
                
                source_stem = md_file.stem.lower()
                
                for target in linked_targets:
                    # target 파일에 대한 백링크로 source 추가
                    self.backlinks[target].add(source_stem)
                
            except Exception as e:
                print(f"❌ Error analyzing {md_file}: {e}")
        
        print(f"📊 Found backlinks for {len(self.backlinks)} pages")
    
    def _generate_backlink_section(self, target_file: Path) -> str:
        """백링크 섹션 생성"""
        target_stem = target_file.stem.lower()
        
        if target_stem not in self.backlinks or not self.backlinks[target_stem]:
            return ""
        
        section = "\n---\n\n## 이 문서를 참조하는 문서들\n\n"
        
        # 백링크 정렬
        sorted_backlinks = sorted(self.backlinks[target_stem])
        
        for source_stem in sorted_backlinks:
            if source_stem in self.file_map:
                source_file = self.file_map[source_stem]
                title = self.title_map.get(source_file, source_stem)
                
                relative_path = source_file.relative_to(self.wiki_dir)
                url_path = str(relative_path.with_suffix('')).replace('\\', '/')
                
                section += f"- [{title}](/wiki/{url_path}/)\n"
        
        return section
    
    def update_file_backlinks(self, file_path: Path) -> bool:
        """파일에 백링크 섹션 추가/업데이트"""
        try:
            content = file_path.read_text(encoding='utf-8')
            front_matter, body = self._extract_front_matter(content)
            
            # 기존 백링크 섹션 제거
            body = re.sub(
                r'\n---\n\n## 이 문서를 참조하는 문서들\n\n.*?(?=\n---\n|\Z)',
                '',
                body,
                flags=re.DOTALL
            )
            
            # 새 백링크 섹션 생성
            backlink_section = self._generate_backlink_section(file_path)
            
            # 내용 조합
            if front_matter:
                new_content = f"---{front_matter}---{body}{backlink_section}"
            else:
                new_content = f"{body}{backlink_section}"
            
            if new_content != content:
                file_path.write_text(new_content, encoding='utf-8')
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
            return False
    
    def generate_all(self):
        """모든 파일에 백링크 생성"""
        if not self.wiki_dir.exists():
            print(f"⚠️  {self.wiki_dir} directory not found")
            return
        
        print(f"🔍 Building file map...")
        self._build_file_map()
        
        print(f"📚 Found {len(self.file_map)} wiki files")
        
        self.analyze_links()
        
        print("✍️  Updating backlinks...")
        print("-" * 50)
        
        updated_count = 0
        for md_file in self.wiki_dir.rglob("*.md"):
            if md_file.name == "index.md":
                continue
            
            if self.update_file_backlinks(md_file):
                backlink_count = len(self.backlinks.get(md_file.stem.lower(), []))
                print(f"✅ Updated: {md_file} ({backlink_count} backlinks)")
                updated_count += 1
            else:
                print(f"⏭️  Skipped: {md_file} (no changes)")
        
        print("-" * 50)
        print(f"✨ Backlink generation complete: {updated_count} files updated")

def main():
    print("=" * 50)
    print("Backlink Generator")
    print("=" * 50)
    
    generator = BacklinkGenerator()
    generator.generate_all()
    
    print("=" * 50)

if __name__ == "__main__":
    main()
