import os
import re
from pathlib import Path

def main():
    target_dir = Path("/Users/aditya1981/Documents/Unified Data Ingestion Engine/frontend/src/features/forecast/components/widgets")
    count = 0
    
    for filepath in target_dir.rglob("*.tsx"):
        content = filepath.read_text(encoding='utf-8')
        
        # Replace simple import React from 'react';
        new_content = re.sub(r"^import\s+React\s+from\s+['\"]react['\"];?\n", "", content, flags=re.MULTILINE)
        
        # Handle import React, { useState } from 'react'; -> import { useState } from 'react';
        new_content = re.sub(r"^import\s+React\s*,\s*{\s*([^}]+)\s*}\s+from\s+['\"]react['\"];?\n", r"import { \1 } from 'react';\n", new_content, flags=re.MULTILINE)

        # Handle import { ..., FC, ... } from 'react' if FC is unused, but we'll leave it for now if tsc doesn't complain about FC
        
        if content != new_content:
            filepath.write_text(new_content, encoding='utf-8')
            count += 1
            print(f"Fixed: {filepath.name}")

    print(f"Fixed {count} files.")

if __name__ == '__main__':
    main()
