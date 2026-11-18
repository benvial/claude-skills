#!/usr/bin/env python3
"""Copy external skills into the plugin at the commits pinned in vendor.json.

Usage:
    python scripts/sync.py           # materialize the pinned commits
    python scripts/sync.py --bump    # move every pin to upstream HEAD, then materialize

Only paths listed in vendor.json are written. Paths this script wrote on a
previous run but that are no longer listed are deleted; everything else under
plugins/skills/ (the own skills) is left alone. The list of written paths is
kept in plugins/skills/.vendored.json.
"""

import argparse
import io
import json
import os
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "vendor.json"
PLUGIN = ROOT / "plugins" / "skills"
STATE = PLUGIN / ".vendored.json"
LICENSES = ROOT / "LICENSES"


def _request(url: str) -> urllib.request.Request:
    headers = {"User-Agent": "claude-skills-sync"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers)


def head_sha(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}/commits/HEAD"
    with urllib.request.urlopen(_request(url)) as response:
        return json.load(response)["sha"]


def fetch(repo: str, ref: str) -> tarfile.TarFile:
    url = f"https://codeload.github.com/{repo}/tar.gz/{ref}"
    with urllib.request.urlopen(_request(url)) as response:
        data = response.read()
    return tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")


def extract(archive: tarfile.TarFile, src: str, dest: Path) -> None:
    """Copy file or directory `src` (relative to the repo root) to `dest`."""
    found = False
    for member in archive.getmembers():
        # Archive entries are "<repo>-<sha>/<path>".
        _, _, rel = member.name.partition("/")
        if rel != src and not rel.startswith(src + "/"):
            continue
        if not (member.isfile() or member.isdir()):
            continue  # symlinks and devices are never copied
        found = True
        target = dest / rel[len(src) :].lstrip("/") if rel != src else dest
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.extractfile(member) as fh:
            target.write_bytes(fh.read())
        if member.mode & 0o111:
            target.chmod(0o755)
    if not found:
        sys.exit(f"error: {src} not found in archive")


def remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--bump", action="store_true", help="move pins to upstream HEAD first")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    if args.bump:
        for name, up in manifest.items():
            sha = head_sha(up["repo"])
            if sha != up["ref"]:
                print(f"{name}: {up['ref'][:7]} -> {sha[:7]}")
                up["ref"] = sha
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")

    previous = set(json.loads(STATE.read_text())) if STATE.exists() else set()
    written: list[str] = []
    for name, up in manifest.items():
        archive = fetch(up["repo"], up["ref"])
        skills = dict(up.get("skills", {}))
        if "plugin" in up:
            # Take every skill the upstream plugin ships, so additions and
            # removals upstream arrive with the next bump.
            member = archive.getmember(f"{archive.getnames()[0].split('/')[0]}/{up['plugin']}")
            with archive.extractfile(member) as fh:
                for path in json.load(fh)["skills"]:
                    path = path.removeprefix("./").rstrip("/")
                    skills.setdefault(Path(path).name, path)
        for dest_name, src in skills.items():
            dest = PLUGIN / "skills" / dest_name
            remove(dest)
            extract(archive, src, dest)
            written.append(str(dest.relative_to(PLUGIN)))
        for dest_name, src in up.get("agents", {}).items():
            dest = PLUGIN / "agents" / dest_name
            remove(dest)
            extract(archive, src, dest)
            written.append(str(dest.relative_to(PLUGIN)))
        lic_dir = LICENSES / name
        remove(lic_dir)
        for lic in up.get("license", []):
            extract(archive, lic, lic_dir / Path(lic).name)
        (lic_dir / "SOURCE").write_text(f"https://github.com/{up['repo']}/tree/{up['ref']}\n")

    for stale in sorted(previous - set(written)):
        print(f"removing {stale} (no longer in vendor.json)")
        remove(PLUGIN / stale)
    for lic_dir in LICENSES.iterdir():
        if lic_dir.name not in manifest:
            remove(lic_dir)
    STATE.write_text(json.dumps(sorted(written), indent=2) + "\n")


if __name__ == "__main__":
    main()
