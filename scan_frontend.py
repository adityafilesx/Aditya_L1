import os
import re
from collections import defaultdict
from pathlib import Path

def scan():
    frontend_dir = Path("/Users/aditya1981/Documents/Unified Data Ingestion Engine/frontend/src")
    
    report = defaultdict(list)
    
    for file_path in frontend_dir.rglob("*.*"):
        if file_path.suffix not in ['.ts', '.tsx']:
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            continue
            
        # Check merge conflicts
        if '<<<<<<< HEAD' in content:
            report['merge_conflicts'].append(str(file_path))
            
        # Check duplicated imports (naive: same line appearing multiple times)
        lines = content.split('\n')
        imports = [line.strip() for line in lines if line.strip().startswith('import ')]
        if len(imports) != len(set(imports)):
            report['duplicated_imports'].append(str(file_path))
            
        # Check duplicated exports (naive: multiple export const <Name> or export function <Name>)
        exports = re.findall(r'export\s+(?:const|function|class)\s+([a-zA-Z0-9_]+)', content)
        if len(exports) != len(set(exports)):
            report['duplicated_exports'].append(str(file_path))
            
        # Check duplicate components / hooks in same file
        components = [e for e in exports if e[0].isupper()]
        if len(components) != len(set(components)):
            report['duplicated_components'].append(str(file_path))
            
        hooks = [e for e in exports if e.startswith('use')]
        if len(hooks) != len(set(hooks)):
            report['duplicated_hooks'].append(str(file_path))
            
        # Empty widgets? Let's see if return is empty or null
        if 'return null;' in content or 'return ();' in content.replace(' ', ''):
            report['empty_components'].append(str(file_path))

    for k, v in report.items():
        print(f"--- {k.upper()} ---")
        for f in set(v):
            print(f)
        print()

if __name__ == '__main__':
    scan()
