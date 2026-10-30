"""Cache version-pinned primary papers and searchable text in this sidecar only."""

import hashlib
import io
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
SOURCES.mkdir(exist_ok=True)
manifest_path = ROOT / "source_manifest.json"
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

for url in sys.argv[1:]:
    name = url.rstrip("/").split("/")[-1]
    kind = "pdf" if "/pdf/" in url or url.endswith(".pdf") else "html"
    name = name.removesuffix(".pdf") + "." + kind
    destination = SOURCES / name
    if not destination.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "bounded-primary-literature-review/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
            resolved_url = response.url
        if kind == "pdf" and not payload.startswith(b"%PDF"):
            raise ValueError(f"Not a PDF: {url}")
        destination.write_bytes(payload)
        manifest[name] = {
            "url": url,
            "resolved_url": resolved_url,
            "retrieved_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
        }
    payload = destination.read_bytes()
    if kind == "pdf":
        reader = PdfReader(io.BytesIO(payload))
        text = "\n\n".join(
            f"=== PDF PAGE {index + 1} ===\n{page.extract_text(extraction_mode='layout')}"
            for index, page in enumerate(reader.pages)
        )
    else:
        soup = BeautifulSoup(payload, "html.parser")
        for math in soup.find_all("math"):
            math.replace_with(" " + math.get("alttext", math.get_text(" ", strip=True)) + " ")
        article = soup.find("article") or soup
        text = article.get_text("\n", strip=True)
    destination.with_suffix(".txt").write_text(text, encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(name, manifest[name]["sha256"], flush=True)
