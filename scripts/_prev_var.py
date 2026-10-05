import sys
sys.path.insert(0, "scripts")
from build_cdf_mix import run
from pathlib import Path
for v in "ABC":
    for t, n in ((13100, "c4"), (16300, "c5")):
        out = Path(f"outputs/_proposta_{v}/chk"); out.mkdir(exist_ok=True)
        print(run("preview", "--help")[:0] if False else "", end="")
