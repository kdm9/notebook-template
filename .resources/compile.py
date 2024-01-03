import markdown
import frontmatter

from pathlib import Path
from concurrent.futures import as_completed, ProcessPoolExecutor
from dataclasses import dataclass
from collections import defaultdict
import os


@dataclass
class Post:
    """One post/dir"""
    path: Path
    attachments: list[str]
    metadata: dict

    def __init__(self, site, indexmd: Path):
        self.path = indexmd
        fm = frontmatter.load(self.path)
        self.metadata = fm.metadata
        self.document = fm.content
        for tag in self.metadata.get("tags", []):
            site.tags[tag].append(self)
        self.attachments = list(self.path.parent.glob("*.ipynb"))

    def output(self, outpath):
        


@dataclass
class Site:
    """Tag for the tagcloud"""
    posts: list[Post] 
    tags: dict[str: list]

    def __init__(self):
        self.exclude_dirs = ("renv", "tmp", ".git", ".ipynb_checkpoints", ".Rproj.user")
        self.posts = []
        self.tags = defaultdict(list)

    def parse(self, dirs):
        for root, dirs, files in os.walk(path):
            if root == path:
                continue
            dirs = list(filter(lambda d: d not in self.exclude_dirs and d.startswith("202"), sorted(dirs)))
            if "index.md" in files:
                file = Path(root) / "index.md"
                p = Post(self, file)
                self.posts.append(p)
            

if __name__ == "__main__":
    s = Site()
    s.parse()
    print(s)
