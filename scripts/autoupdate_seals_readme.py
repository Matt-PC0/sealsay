from pathlib import Path
import re

SEALS   = Path("seals")
README  = Path("README.md") 

descriptions = {}
descriptions_file = SEALS / "descriptions.txt"

if descriptions_file.exists():
    for line in descriptions_file.read_text().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            descriptions[k.strip()] = v.strip()

lines = []

for p in sorted(SEALS.glob("*.txt")):
    if p.name == "descriptions.txt":
        continue
    
    flag = f"-{p.stem[0]}"
    desc = descriptions.get(p.stem, p.stem)
    lines.append(f"{flag}: {desc} seal\n")
    
block = "\n".join(lines)
content = README.read_text()
new = re.sub(
    r"(<!-- SEALS:START -->).*?(<!-- SEALS:END -->)",
    rf"\1\n{block}\n\2",
    content,
    flags=re.DOTALL,
)

README.write_text(new)