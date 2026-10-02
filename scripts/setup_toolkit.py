"""Install an exact toolkit release into a contest-specific virtual environment."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile
from pathlib import Path

try:
    from .build import environment_python
except ImportError:
    from build import environment_python


def wheel_digest(wheel: Path) -> str:
    digest = hashlib.sha256()
    prefix = "kgupc_toolkit/"
    with zipfile.ZipFile(wheel) as package:
        names = [name for name in package.namelist() if name.startswith(prefix)
                 and not name.endswith("/")
                 and (name.startswith(prefix + "resources/")
                      or (name[len(prefix):].endswith(".py") and "/" not in name[len(prefix):]))]
        for name in sorted(names):
            content = package.read(name)
            if Path(name).suffix in (".py", ".tex", ".md", ".txt", ".json"):
                content = content.replace(b"\r\n", b"\n")
            relative = name[len(prefix):].encode("utf-8")
            digest.update(relative + b"\0" + len(content).to_bytes(8, "big") + content)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contest", type=Path)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--source", type=Path, help="Toolkit source checkout; build without changing it")
    inputs.add_argument("--wheel", type=Path, help="Original toolkit wheel release")
    args = parser.parse_args()
    try:
        contest = args.contest.resolve()
        lock = contest / "toolkit.lock.json"
        data = json.loads(lock.read_text(encoding="utf-8"))
        if data.get("schema") != 1:
            raise ValueError("Unsupported toolkit lock schema")
        cache = contest / "build" / "packages"
        cache.mkdir(parents=True, exist_ok=True)
        if args.source:
            source = args.source.resolve()
            if not (source / "pyproject.toml").is_file():
                raise ValueError(f"Not a toolkit source checkout: {source}")
            # Build from a temporary copy; pip must not write into a sibling repository.
            with tempfile.TemporaryDirectory(prefix="package-source-", dir=cache) as temporary:
                snapshot = Path(temporary) / "toolkit"
                shutil.copytree(source, snapshot, ignore=shutil.ignore_patterns(
                    ".git", ".venv", "build", "dist", "__pycache__", "*.egg-info"))
                output = Path(temporary) / "wheels"
                subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-index", "--no-deps",
                                "--no-build-isolation", "--no-cache-dir", "--wheel-dir", str(output),
                                str(snapshot)], check=True)
                built = output / f"kgupc_toolkit-{data['version']}-py3-none-any.whl"
                if wheel_digest(built) != data["package_sha256"]:
                    raise ValueError("Toolkit source differs from the contest lock; the existing environment was not changed.")
                wheel = cache / built.name
                if not wheel.exists():
                    shutil.copyfile(built, wheel)
        else:
            wheel = args.wheel.resolve()
        if wheel_digest(wheel) != data["package_sha256"]:
            raise ValueError("Toolkit wheel differs from the contest lock; the existing environment was not changed.")
        python = environment_python(contest)
        if not python.is_file():
            venv.EnvBuilder(with_pip=True).create(contest / ".venv")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps",
                        "--force-reinstall", str(wheel)], check=True)
        subprocess.run([str(python), "-m", "kgupc_toolkit", "verify-lock", str(lock)], check=True)
        print(f"Toolkit ready: {python}")
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(f"Setup error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
