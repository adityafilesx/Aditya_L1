import os
from collections import defaultdict
from pathlib import Path

def main():
    src_dir = Path("/Users/aditya1981/Documents/Unified Data Ingestion Engine/frontend/src")
    file_map = defaultdict(list)
    
    for filepath in src_dir.rglob("*.*"):
        if filepath.suffix not in ['.ts', '.tsx']:
            continue
        file_map[filepath.name].append(str(filepath))
            
    with open("duplicate_files.md", "w") as f:
        for name, paths in file_map.items():
            if len(paths) > 1:
                f.write(f"### {name}\n")
                for path in paths:
                    f.write(f"- {path}\n")
                f.write("\n")

if __name__ == '__main__':
    main()
