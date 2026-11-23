# SPDX-License-Identifier: Apache-2.0
"""Check proposal metadata, local Markdown link targets, and JSON examples."""

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / "proposals"
STATUSES = {
    "To do", "Draft", "Hold", "Finalizing", "Published", "Implemented",
    "Closed", "Superseded",
}
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
PROPOSAL_DIR = re.compile(rf"(\d{{3}}|draft)-({SLUG})", re.ASCII)
LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")


def main():
    errors = []
    used = {}
    index = (PROPOSALS / "README.md").read_text(encoding="utf-8")
    for directory in sorted(path for path in PROPOSALS.iterdir() if path.is_dir()):
        name = PROPOSAL_DIR.fullmatch(directory.name)
        if name is None:
            errors.append(f"{directory.name}: expected NNN-slug or draft-slug")
            continue
        readme = directory / "README.md"
        if not readme.is_file():
            errors.append(f"{directory.name}: missing README.md")
            continue

        document = readme.read_text(encoding="utf-8")
        metadata = re.search(r"^\| Field \| Value \|\n(?:\|[^\n]*\|\n?)+", document, re.MULTILINE)
        fields = dict(re.findall(
            r"^\|\s*(OTIP|Status|Type|Author|Created)\s*\|\s*([^|\n]+?)\s*\|$",
            metadata[0] if metadata else "", re.MULTILINE,
        ))
        number = name[1]
        expected = "Unassigned" if number == "draft" else f"OTIP-{number}"
        if fields.get("OTIP") != expected:
            errors.append(f"{directory.name}: OTIP must be {expected}")
        if fields.get("Status") not in STATUSES:
            errors.append(f"{directory.name}: missing or unknown Status")
        for field in ("Type", "Author"):
            if not fields.get(field, "").strip():
                errors.append(f"{directory.name}: missing {field}")
        created = fields.get("Created", "")
        try:
            if date.fromisoformat(created).isoformat() != created:
                raise ValueError(created)
        except ValueError:
            errors.append(f"{directory.name}: Created must be YYYY-MM-DD")

        if number != "draft":
            if number in used:
                errors.append(f"{directory.name}: {expected} already used by {used[number]}")
            used[number] = directory.name
            row = rf"^\|\s*\[{expected}\]\({re.escape(directory.name)}/README\.md\)\s*\|[^|\n]+\|\s*{re.escape(fields.get('Status', ''))}\s*\|"
            if not re.search(row, index, re.MULTILINE):
                errors.append(f"{directory.name}: missing or mismatched proposal index row")

    for document in sorted(ROOT.rglob("*.md")):
        if ".git" in document.relative_to(ROOT).parts:
            continue
        for link in LINK.findall(document.read_text(encoding="utf-8")):
            target = urlsplit(link)
            if target.scheme or target.netloc or not target.path:
                continue
            resolved = (document.parent / unquote(target.path)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{document.relative_to(ROOT)}: broken local link {link}")

    for example in sorted(PROPOSALS.rglob("*")):
        if not example.is_file() or example.suffix not in {".json", ".otio"}:
            continue
        try:
            json.loads(example.read_text(encoding="utf-8"))
        except ValueError as error:
            errors.append(f"{example.relative_to(ROOT)}: {error}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Proposal metadata, relative links and example JSON passed.")


if __name__ == "__main__":
    main()
