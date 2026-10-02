"""Integration check for split sections, literal examples, notes and dependency watching."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "2025/.venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def text(path):
    return subprocess.check_output(["pdftotext", "-layout", str(path), "-"]).decode("utf-8")


def main():
    logs = ROOT / "2025/problems/build/polygon-verification"
    logs.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".polygon-check-", dir=ROOT / "build") as temporary:
        assert Path(temporary).resolve().is_relative_to((ROOT / "build").resolve())
        directory = Path(temporary) / "problems"
        directory.mkdir()
        for name in ("main.tex", "problem-list.tex"):
            shutil.copyfile(ROOT / "2025/problems" / name, directory / name)
        # Keep the two-problem edit fixture independent of new archive registrations.
        (directory / "problem-list.tex").write_text("".join(
            f"\\includeproblem{{{letter}}}{{{next((ROOT / '2025/problems' / letter).glob('*.tex')).name}}}\n"
            for letter in ("A", "B")), encoding="utf-8")
        shutil.copytree(ROOT / "2025/problems/A", directory / "A", ignore=shutil.ignore_patterns("*.pdf"))
        shutil.copytree(ROOT / "2025/problems/B", directory / "B", ignore=shutil.ignore_patterns("*.pdf"))
        sections = directory / "A/statement-sections/korean"
        combined = directory / "main.pdf"
        a = directory / "A/kgu-solutio-kgu-ai-cse.pdf"
        b = directory / "B/parking-fee-system.pdf"

        def build(source, label):
            with (logs / f"{label}.log").open("wb") as output:
                result = subprocess.run([str(PYTHON), "-m", "kgupc_toolkit", "build", str(source),
                                         "--lock", str(ROOT / "2025/toolkit.lock.json")],
                                        stdout=output, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f"Build failed: {logs / (label + '.log')}")

        build(sections / "legend.tex", "initial")
        assert "예제 설명" not in text(a)
        b_hash = hashlib.sha256(b.read_bytes()).hexdigest()
        b_timestamp = b.stat().st_mtime_ns
        with (sections / "legend.tex").open("a", encoding="utf-8") as source:
            source.write("\nPOLYGON-LEGEND-MARKER\n")
        (sections / "notes.tex").write_text("POLYGON-NOTES-MARKER\n", encoding="utf-8")
        (sections / "tutorial.tex").write_text("SECRET-SOLUTION\n", encoding="utf-8")
        (sections / "example.02").write_text("2026\n", encoding="utf-8")
        (sections / "example.03").write_text("literal_#%{}\n1  2\n", encoding="utf-8")
        (sections / "example.03.a").write_text("OK\n", encoding="utf-8")
        # This example must use full-width breakable boxes rather than an overflowing minipage.
        (sections / "example.04").write_text("\n".join(f"LONG-{n:03d}" for n in range(70)) + "\n",
                                             encoding="utf-8")
        (sections / "example.04.a").write_text("LONG-ANSWER\n", encoding="utf-8")
        metadata = directory / "A/statement.json"
        info = json.loads(metadata.read_text(encoding="utf-8"))
        info["timeLimit"] = 1500
        metadata.write_text(json.dumps(info), encoding="utf-8")
        build(sections / "example.02", "changed")
        for pdf in (combined, a):
            content = text(pdf)
            # Some TeX font mappings extract the code hyphen as U+2011.
            normalized = content.replace("\u2011", "-")
            (logs / ("changed-combined.txt" if pdf == combined else "changed-A.txt")).write_text(content, encoding="utf-8")
            shutil.copyfile(pdf, logs / ("changed-combined.pdf" if pdf == combined else "changed-A.pdf"))
            for expected in ("POLYGON-LEGEND-MARKER", "POLYGON-NOTES-MARKER", "2026",
                             "literal_#%{}", "LONG-069", "LONG-ANSWER", "1.5초"):
                assert expected in normalized or expected in "".join(normalized.split()), expected
            assert "SECRET-SOLUTION" not in content
            assert "1108" not in content
        assert hashlib.sha256(b.read_bytes()).hexdigest() == b_hash
        assert b.stat().st_mtime_ns == b_timestamp
        dependencies = (directory / "main.fls").read_text(encoding="utf-8").lower()
        for name in ("statement.json", "notes.tex", "example.02", "name.tex"):
            assert name in dependencies, f"Missing recorded dependency: {name}"
        generated = (directory / "build/statements/A.tex").read_text(encoding="utf-8")
        assert r"\SampleFileStack{4}" in generated
        # Deletion and empty notes must remove old generated content on the next build.
        (sections / "notes.tex").write_text("", encoding="utf-8")
        for name in ("example.03", "example.03.a", "example.04", "example.04.a"):
            (sections / name).unlink()
        build(metadata, "removed")
        assert "POLYGON-NOTES-MARKER" not in text(a)
        assert "예제 설명" not in text(a)
        assert "literal_#%{}" not in text(a)
        assert "LONG-069" not in text(a).replace("\u2011", "-")
        shutil.copyfile(a, logs / "sample-A.pdf")
        print("PASS: split edits, sample addition/removal, literal text, long examples, optional notes,")
        print("      fractional limits, no solution leakage, .fls dependencies and unchanged B")


if __name__ == "__main__":
    main()
