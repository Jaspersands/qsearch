"""Compare pinned primary sections while retaining LaTeX formula content."""

from hashlib import sha256
import json
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
SECTIONS = ("S3.SS2", "S5.SS1", "S5.SS2", "S5.SS3", "S5")


def read_version(version):
    path = ROOT / f"primary-2610.00502v{version}.html"
    raw = path.read_bytes()
    soup = BeautifulSoup(raw, "html.parser")
    assert f"arXiv:2610.00502v{version}" in soup.get_text(" ", strip=True)
    for math in soup.find_all("math"):
        assert math.get("alttext") is not None
        math.replace_with(math["alttext"])
    sections = {}
    for identifier in SECTIONS:
        section = soup.find(id=identifier)
        assert section is not None
        sections[identifier] = " ".join(section.get_text(" ", strip=True).split())
    return {"url": f"https://arxiv.org/html/2610.00502v{version}",
            "raw_html_sha256": sha256(raw).hexdigest()}, sections


v1, text1 = read_version(1)
v2, text2 = read_version(2)
comparisons = {}
for section in SECTIONS:
    assert text1[section] == text2[section], section
    comparisons[section] = {"identical_normalized_text_and_math": True,
                            "characters": len(text1[section]),
                            "sha256": sha256(text1[section].encode()).hexdigest()}
report = {"checked_date": "2026-10-26", "versions": {"v1": v1, "v2": v2},
          "latest_version_listed_on_arxiv_abstract_page": "v2",
          "v2_submission_time_utc": "2026-10-02T15:23:05Z",
          "normalization": "Replace MathML with its LaTeX alttext; collapse whitespace; compare section text.",
          "sections": comparisons,
          "conclusion": "No v2 change to these reduction/quantum-decoder sections; no novelty inference."}
(ROOT / "version-comparison.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
