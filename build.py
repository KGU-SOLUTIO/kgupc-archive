"""Build with the toolkit pinned by the selected contest."""
import json
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent


def toolkit_python(lock):
    data = json.loads(lock.read_text(encoding='utf-8'))
    environment = ROOT / '.venv' / 'toolkits' / data['package_sha256']
    python = environment / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    ready = environment / '.toolkit-ready'
    if not ready.is_file():
        print(f"Installing kgupc-toolkit {data['version']} for {lock.parent.name}", flush=True)
        if not python.is_file():
            venv.create(environment, with_pip=True)
        try:
            subprocess.run([str(python), '-m', 'pip', 'install',
                            f"git+{data['repository']}@{data['revision']}"], check=True)
        except subprocess.CalledProcessError:
            print(f'Installation failed. Retry with: {python} -m pip install '
                  f"git+{data['repository']}@{data['revision']}", file=sys.stderr)
            raise
    subprocess.run([str(python), '-m', 'kgupc_toolkit', 'verify-lock', str(lock)], check=True)
    ready.touch()
    return python


def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: python build.py <source.tex> | --setup')
    if sys.argv[1] == '--setup':
        for lock in sorted(ROOT.glob('*/toolkit.lock.json')):
            toolkit_python(lock)
        return
    source = Path(sys.argv[1]).resolve()
    if not source.suffix:
        source = source.with_suffix('.tex')
    lock = next((p / 'toolkit.lock.json' for p in source.parents
                 if (p / 'toolkit.lock.json').is_file()), None)
    if lock is None or lock.parent.parent != ROOT:
        sys.exit('No contest toolkit.lock.json found for this source.')
    python = toolkit_python(lock)
    subprocess.run([str(python), '-m', 'kgupc_toolkit', 'build', str(source)], check=True)


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
