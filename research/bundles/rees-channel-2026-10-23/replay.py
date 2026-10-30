import hashlib
import json
from pathlib import Path

from physical_channel import audit


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    report = audit()
    report["source_hashes"] = {
        name: hashlib.sha256((root/name).read_bytes()).hexdigest()
        for name in ("physical_channel.py", "test_physical_channel.py", "replay.py", "REES_CHANNEL_AUDIT.md")}
    output = root/"rees_channel_receipt.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ("source_hashes", "all_positive_adaptive_label_tuples")}, indent=2))
