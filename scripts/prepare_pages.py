"""Copy committed contest booklets and editorials into the Pages artifact."""

from html import escape
from pathlib import Path
import re
import shutil


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    destination = root / "build" / "pages"
    destination.mkdir(parents=True, exist_ok=True)
    links = []

    for contest in sorted(root.iterdir()):
        if not contest.is_dir() or not re.fullmatch(r"\d{4}(?:-(?:advanced|beginner))?", contest.name):
            continue
        for section, label in (("problems", "문제집"), ("solutions", "에디토리얼")):
            source = contest / section / "main.pdf"
            if not source.is_file():
                continue
            relative = source.relative_to(root)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            links.append(f'<li><a href="{relative.as_posix()}">{escape(contest.name)} {label}</a></li>')

    if not links:
        raise RuntimeError("No contest PDFs found. Build the PDFs before publishing.")

    (destination / ".nojekyll").touch()
    (destination / "index.html").write_text(
        '<!doctype html>\n<html lang="ko">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>KGUPC Archive</title>\n<h1>KGUPC Archive</h1>\n<ul>\n'
        + "\n".join(links) + "\n</ul>\n</html>\n",
        encoding="utf-8",
    )
    print(f"Prepared {len(links)} PDFs in {destination}")


if __name__ == "__main__":
    main()
