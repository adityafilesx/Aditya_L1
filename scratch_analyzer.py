import os
import re
from pathlib import Path

def analyze_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    issues = []
    
    # 1. Merge conflicts
    if '<<<<<<<' in content or '=======' in content or '>>>>>>>' in content:
        issues.append("Merge conflict markers found")
        
    # 2. Duplicate imports
    imports = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('import '):
            if line in imports:
                issues.append(f"Duplicate import: {line}")
            else:
                imports.append(line)
                
    # 3. Duplicate exports (components/hooks)
    exports = []
    # match `export const Name` or `export function Name`
    export_pattern = re.compile(r'export\s+(?:const|function|class)\s+([a-zA-Z0-9_]+)')
    for match in export_pattern.finditer(content):
        name = match.group(1)
        if name in exports:
            if name.startswith('use'):
                issues.append(f"Duplicate hook export: {name}")
            elif name[0].isupper():
                issues.append(f"Duplicate component export: {name}")
            else:
                issues.append(f"Duplicate export: {name}")
        else:
            exports.append(name)
            
    # 4. Duplicate JSX returns (often a sign of a bad auto-generation or merge)
    returns = re.findall(r'return\s*\(\s*(<[a-zA-Z0-9_]+[^>]*>.*?</[a-zA-Z0-9_]+>)\s*\)', content, re.DOTALL)
    if len(returns) > 1 and returns[0] == returns[1]:
        issues.append("Duplicate JSX returns found")
        
    return issues

def main():
    src_dir = Path("/Users/aditya1981/Documents/Unified Data Ingestion Engine/frontend/src")
    report = []
    
    for filepath in src_dir.rglob("*.*"):
        if filepath.suffix not in ['.ts', '.tsx']:
            continue
            
        issues = analyze_file(filepath)
        if issues:
            report.append(f"### {filepath.relative_to(src_dir.parent)}\n")
            for issue in issues:
                report.append(f"- {issue}\n")
            report.append("\n")
            
    with open("analyzer_report.md", "w") as f:
        f.writelines(report)

if __name__ == '__main__':
    main()
