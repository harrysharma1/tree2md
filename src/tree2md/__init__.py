import json
import os
import subprocess

from tree2md.tree import Root

FILE_ICON = {
    "py": ""        
}

EXCLUDES = ".git|__pycache__|.venv"

def main() -> None:
    proc = subprocess.run(
        ["tree", "-J", "--noreport", "--dirsfirst", "--charset=utf-8", "-I", EXCLUDES],
        text=True, capture_output=True, check=True,
    )
    root = Root.from_dict(json.loads(proc.stdout))

    lines = [f"📁{root.name}/"]
    for node, depth in root.walk():
        line = f'{"   " * (depth - 1)} * {"📁" if node.is_dir else "📄"}{node.name}{"/" if node.is_dir else ""}' 
        lines.append(line)
    print("\n".join(lines))
