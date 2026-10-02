"""Dispatch a contest build to that contest's locked toolkit environment."""

import argparse
import subprocess
import sys
from pathlib import Path


def contest_directory(source: Path) -> Path:
    source = source.resolve()
    directory = source if source.is_dir() else source.parent
    for parent in (directory, *directory.parents):
        if (parent / "toolkit.lock.json").is_file():
            return parent
    raise ValueError("No toolkit.lock.json found for this contest. Set up its toolkit dependency first.")


def environment_python(contest: Path) -> Path:
    folder = "Scripts" if sys.platform == "win32" else "bin"
    filename = "python.exe" if sys.platform == "win32" else "python"
    return contest / ".venv" / folder / filename


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    try:
        source = args.source.resolve()
        contest = contest_directory(source)
        python = environment_python(contest)
        if not python.is_file():
            raise ValueError(f"Toolkit environment missing: {python}. "
                             "Run scripts/setup_toolkit.py with the original toolkit release.")
        return subprocess.run([str(python), "-m", "kgupc_toolkit", "build", str(source),
                               "--lock", str(contest / "toolkit.lock.json")]).returncode
    except (ValueError, OSError) as error:
        print(f"Build error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
