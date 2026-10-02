"""Optional integration check: real PDFs, shared edits, samples, images and headers.

Run from the repository root: python tests/verify_pdfs.py
Requires XeLaTeX, latexmk and pdftotext. Uses an isolated temporary contest.
"""

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "2025" / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def pdf_text(path):
    result = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                            check=True, capture_output=True)
    return result.stdout.decode("utf-8")


def run_build(source, log):
    with log.open("wb") as output:
        result = subprocess.run([str(PYTHON), "-m", "kgupc_toolkit", "build", str(source),
                                 "--lock", str(ROOT / "2025" / "toolkit.lock.json")],
                                stdout=output, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Build failed; see {log}")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    for command in ("xelatex", "latexmk", "pdftotext"):
        if not shutil.which(command):
            raise RuntimeError(f"Missing tool: {command}")
    logs = ROOT / "2025" / "problems" / "build" / "verification"
    logs.mkdir(parents=True, exist_ok=True)
    # Deliberately use a different directory depth from 2025: templates come from the package.
    with tempfile.TemporaryDirectory(prefix=".pdf-check-", dir=ROOT / "build") as temporary:
        contest = Path(temporary).resolve()
        require(contest.is_relative_to(ROOT), "Temporary contest must stay in the workspace")
        directory = contest / "problems"
        directory.mkdir()
        original = ROOT / "2025" / "problems"
        for filename in ("main.tex", "problem-list.tex"):
            shutil.copyfile(original / filename, directory / filename)
        # This pagination fixture intentionally contains only A and B.
        # The real archive manifest can grow independently (2025 now has A through G).
        (directory / "problem-list.tex").write_text("".join(
            f"\\includeproblem{{{letter}}}{{{next((original / letter).glob('*.tex')).name}}}\n"
            for letter in ("A", "B")), encoding="utf-8")
        for letter in ("A", "B"):
            (directory / letter).mkdir()
            for source in (original / letter).glob("*.tex"):
                # Keep pagination checks independent of real statements as they grow.
                (directory / letter / source.name).write_text(
                    f"\\problemheader{{{letter}}}{{검증 문제 {letter}}}\n"
                    "\\problemlimits{}{}\n검증용 본문입니다.\n", encoding="utf-8")

        run_build(directory / "main.tex", logs / "initial.log")
        combined = directory / "main.pdf"
        individual_a = next((directory / "A").glob("*.tex")).with_suffix(".pdf")
        individual_b = next((directory / "B").glob("*.tex")).with_suffix(".pdf")
        require(len(pdf_text(combined).split("\f")) - 1 == 3, "Expected cover + A + B")
        initial_pages = [page for page in pdf_text(combined).split("\f") if page.strip()]
        require(initial_pages[1].strip().splitlines()[-1].strip() == "1", "A must start at page 1")
        require(initial_pages[2].strip().splitlines()[-1].strip() == "2", "B must follow A numbering")
        require("Problem B" not in pdf_text(individual_a), "A PDF contains B")
        require("Problem A" not in pdf_text(individual_b), "B PDF contains A")
        b_hash = hashlib.sha256(individual_b.read_bytes()).hexdigest()
        b_timestamp = individual_b.stat().st_mtime_ns

        images = directory / "A" / "images"
        images.mkdir()
        resources = Path(subprocess.check_output([str(PYTHON), "-m", "kgupc_toolkit", "resources"],
                                                text=True).strip())
        shutil.copyfile(resources / "images" / "logo.png", images / "logo.png")
        statement = next((directory / "A").glob("*.tex"))
        with statement.open("a", encoding="utf-8") as source:
            source.write(r"""
\problemlimits{1}{512}
ARCHIVE-SYNC-MARKER
\includegraphics[width=1cm]{images/logo.png}
\SampleSection
\begin{SampleInput}[2]
1  2
literal_#%{}
\end{SampleInput}
\begin{SampleOutput}[2]
3
\end{SampleOutput}
\newpage
ARCHIVE-A-CONTINUED
""")
        run_build(statement, logs / "changed.log")
        combined_text = pdf_text(combined)
        a_text = pdf_text(individual_a)
        b_text = pdf_text(individual_b)
        for text in (combined_text, a_text):
            require("ARCHIVE-SYNC-MARKER" in text, "Edited A did not reach both PDFs")
            require("ARCHIVE-A-CONTINUED" in text, "Continuation page was lost")
            require("literal_#%{}" in text, "Sample special characters changed")
            require("예제 입력 2" in text and "예제 출력 2" in text, "Missing sample titles")
            require("512MB" in text, "Missing problem limits")
            require("시간 제한: 1초 | 메모리 제한: 512MB" in " ".join(text.split()),
                    "Numeric limits must add units and the separator")
        require("ARCHIVE-SYNC-MARKER" not in b_text, "A edit leaked into B")
        require(hashlib.sha256(individual_b.read_bytes()).hexdigest() == b_hash,
                "Unchanged B PDF was rewritten")
        require(individual_b.stat().st_mtime_ns == b_timestamp,
                "Unchanged published B PDF timestamp changed")
        pages = [page for page in combined_text.split("\f") if page.strip()]
        require(len(pages) == 4, "Expected cover + two A pages + B")
        for page in pages[1:3]:
            require("Problem A" in page.splitlines()[0], "A page has the wrong header")
        require("Problem B" in pages[3].splitlines()[0], "B page has the wrong header")
        for number, page in enumerate(pages[1:], 1):
            require(page.strip().splitlines()[-1].strip() == str(number),
                    "Combined page numbering must start at A and continue across problems")
        require(len(a_text.split("\f")) - 1 == 2, "Individual A has unexpected pages")

        # Keep a reviewable copy of the test PDFs, away from the real statements.
        for source, name in ((combined, "sample-combined.pdf"),
                             (individual_a, "sample-A.pdf")):
            shutil.copyfile(source, logs / name)
        print("PASS: shared edit, independent PDFs, unchanged B, multipage headers, images and samples")
        print(f"Verification artifacts: {logs}")


if __name__ == "__main__":
    main()
