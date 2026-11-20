"""Xcode build phase. Package the checked-in production game and verify its offline resources."""
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import plistlib
import re
import sqlite3
import subprocess
from urllib.parse import parse_qs, unquote, urlsplit


class GamePage(HTMLParser):
    def __init__(self, path, root):
        super().__init__()
        self.path = path
        self.root = root
        self.stories = set()

    def resource(self, address):
        return resource(self.root, self.path, address)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "src" in attrs:
            self.resource(attrs["src"])
        if "href" in attrs:
            href = attrs["href"]
            if tag == "a" and urlsplit(href).scheme in ("http", "https"):
                return
            self.resource(href)
        if "data-story" in attrs:
            story = self.resource(attrs["data-story"])
            if parse_qs(urlsplit(attrs["href"]).query).get("story") != [attrs["data-story"]]:
                raise ValueError(f"Catalogue link does not match {story}")
            self.stories.add(story)


def resource(root, source, address):
    url = urlsplit(address)
    path = unquote(url.path)
    target = (source.parent / path).resolve()
    if (url.scheme or url.netloc or not path or path.startswith("/") or
            root not in target.parents or not target.is_file()):
        raise ValueError(f"{source.relative_to(root)} references an unavailable bundled file: {address}")
    return target


def audit(root):
    stories = set()
    for name in ("index.html", "make-something.html"):
        page = GamePage(root / name, root)
        page.feed(page.path.read_text())
        stories.update(page.stories)
    manuscripts = {p for p in (root / "stories").rglob("*.md") if p.name.lower() != "design-brief.md"}
    if not stories or stories != manuscripts:
        raise ValueError("Bundled manuscripts and the production catalogue differ. Run npm run build.")
    for story in stories:
        for image in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", story.read_text()):
            resource(root, story, image)
    for asset in json.loads((root / "assets/build-files.json").read_text()):
        resource(root, root / "index.html", asset)


def write_build_version(derived, info_template):
    # Archive and Clean discard intermediates. Keep one transactional counter
    # per app on this Mac so concurrent simulator builds and archives share it.
    state = Path.home() / "Library/Application Support" / os.environ["PRODUCT_BUNDLE_IDENTIFIER"] / "Xcode"
    state.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(state / "builds.sqlite3", timeout=30) as db:
        db.execute("CREATE TABLE IF NOT EXISTS builds (id INTEGER PRIMARY KEY, number INTEGER NOT NULL)")
        db.execute("INSERT INTO builds VALUES (1, 1) ON CONFLICT(id) DO UPDATE SET number = number + 1")
        number = db.execute("SELECT number FROM builds WHERE id = 1").fetchone()[0]
    info = plistlib.loads(info_template.read_bytes())
    info["CFBundleVersion"] = str(number)
    (derived / "BuildInfo.plist").write_bytes(plistlib.dumps(info))


if __name__ == "__main__":
    repo = Path(os.environ["SRCROOT"]).parent
    website = (Path(os.environ["TARGET_BUILD_DIR"]) / os.environ["UNLOCALIZED_RESOURCES_FOLDER_PATH"] / "Website").resolve()
    website.mkdir(parents=True, exist_ok=True)
    subprocess.run(["/usr/bin/rsync", "-a", "--delete", "--exclude=.DS_Store", "--exclude=._*",
                    "index.html", "make-something.html", "assets", "stories", str(website)], cwd=repo, check=True)
    audit(website)
    write_build_version(Path(os.environ["DERIVED_FILE_DIR"]), repo / "ios/Game/Info.plist")
