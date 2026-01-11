#!/usr/bin/env python3
"""
Wiki Link Processor
[[wikilink]] 형태를 [wikilink](/wiki/path/) 형태로 변환합니다.
"""

import re
import os
from pathlib import Path
from typing import Dict, Optional

class WikiLinkProcessor:
    def __init__(self, wiki_dir: str = "_wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.file_map: Dict[str, Path] = {}
        self._build_file_map()
    
    def _build_file_map(self):
        """위키 디렉토리의 모든 마크다운 파일 맵 생성"""
        if not self.wiki_dir.exists():
            print(f"⚠️  Warning: {self.wiki_dir} directory not found")
            return
        
        for md_file in self.wiki_dir.rglob("*.md"):
            if md_file.name == "index.md":
                continue
            
            # 파일명과 제목으로 매핑
            file_stem = md_file.stem.lower()
            self.file_map[file_stem] = md_file
            
            # 파일의 title도 매핑 (front matter에서 추출)
            title = self._extract_title(md_file)
            if title:
                self.file_map[title.lower()] = md_file
    
    def _extract_title(self, file_path: Path) -> Optional[str]:
        """마크다운 파일에서 title 추출"""
        try:
            content = file_path.read_text(encoding='utf-8')
            if content.startswith('---'):
                front_matter = content.split('---')[1]
                title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', 
                                      front_matter, re.MULTILINE)
                if title_match:
                    return title_match.group(1).strip()
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
        return None
    
    def _find_wiki_file(self, link_text: str) -> Optional[Path]:
        """링크 텍스트로 실제 파일 찾기"""
        link_lower = link_text.lower().strip()
        return self.file_map.get(link_lower)
    
    def _convert_to_url(self, file_path: Path) -> str:
        """파일 경로를 URL로 변환"""
        relative_path = file_path.relative_to(self.wiki_dir)
        url_path = str(relative_path.with_suffix('')).replace('\\', '/')
        return f"/wiki/{url_path}/"
    
    def process_wikilinks(self, content: str) -> tuple[str, int]:
        """
        [[wikilink]] 형태를 마크다운 링크로 변환
        
        Returns:
            (변환된 내용, 변환된 링크 수)
        """
        conversion_count = 0
        
        def replace_link(match):
            nonlocal conversion_count
            full_match = match.group(0)
            link_text = match.group(1).strip()
            
            # 파일 찾기
            wiki_file = self._find_wiki_file(link_text)
            
            if wiki_file:
                url = self._convert_to_url(wiki_file)
                conversion_count += 1
                return f"[{link_text}]({url})"
            else:
                # 파일을 찾지 못하면 원본 유지 (나중에 생성할 수 있음)
                print(f"⚠️  Link target not found: [[{link_text}]]")
                return full_match
        
        # [[링크]] 패턴 찾아서 변환
        converted = re.sub(r'\[\[([^\]]+)\]\]', replace_link, content)
        return converted, conversion_count
    
    def process_file(self, file_path: Path) -> bool:
        """단일 파일 처리"""
        try:
            original_content = file_path.read_text(encoding='utf-8')
            converted_content, count = self.process_wikilinks(original_content)
            
            if converted_content != original_content:
                file_path.write_text(converted_content, encoding='utf-8')
                print(f"✅ Processed: {file_path} ({count} links converted)")
                return True
            else:
                print(f"⏭️  Skipped: {file_path} (no wikilinks found)")
                return False
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return False
    
    def process_all(self):
        """모든 위키 파일 처리"""
        if not self.wiki_dir.exists():
            print(f"📁 Creating {self.wiki_dir} directory")
            self.wiki_dir.mkdir(parents=True, exist_ok=True)
            return
        
        print(f"🔍 Searching for wiki files in {self.wiki_dir}")
        md_files = list(self.wiki_dir.rglob("*.md"))
        
        if not md_files:
            print("📝 No markdown files found")
            return
        
        print(f"📚 Found {len(md_files)} markdown files")
        print(f"🗺️  Built file map with {len(self.file_map)} entries")
        print("-" * 50)
        
        processed_count = 0
        for md_file in md_files:
            if self.process_file(md_file):
                processed_count += 1
        
        print("-" * 50)
        print(f"✨ Processing complete: {processed_count}/{len(md_files)} files updated")

def main():
    print("=" * 50)
    print("Wiki Link Processor")
    print("=" * 50)
    
    processor = WikiLinkProcessor()
    processor.process_all()
    
    print("=" * 50)

if __name__ == "__main__":
    main()
