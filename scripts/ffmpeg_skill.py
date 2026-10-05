"""Run the pinned project-local ffmpeg-skill with the current Python interpreter."""
from pathlib import Path
import re
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    scripts = root / '.agents' / 'skills' / 'ffmpeg-skill' / 'scripts'
    if len(sys.argv) < 2:
        print('Usage: python scripts/ffmpeg_skill.py TOOL [ARGS]')
        print('Examples: probe INPUT.mp4 --compact; doctor --json; contract --json')
        return 2
    tool, args = sys.argv[1], sys.argv[2:]
    if tool in ('doctor', 'contract'):
        script = scripts / '_contract.py'
        args = (['doctor'] if tool == 'doctor' else []) + args
    else:
        if not re.fullmatch(r'[a-z][a-z0-9_]*', tool):
            print('Invalid tool name.', file=sys.stderr)
            return 2
        script = scripts / (tool + '.py')
    if not script.is_file():
        print('Tool is not installed: ' + tool, file=sys.stderr)
        return 2
    return subprocess.run([sys.executable, str(script), *args], shell=False).returncode


if __name__ == '__main__':
    raise SystemExit(main())
