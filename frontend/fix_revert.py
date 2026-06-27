import os

def fix_revert(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Revert title to label for DataDisplay
    content = content.replace('<DataDisplay title=', '<DataDisplay label=')
    content = content.replace('<MetricCard title=', '<MetricCard label=')
    content = content.replace('<Slider title=', '<Slider label=')
    content = content.replace('<Checkbox title=', '<Checkbox label=')
    
    with open(filepath, 'w') as f:
        f.write(content)

src_dir = '/Users/aditya1981/Documents/Unified Data Ingestion Engine/frontend/src'
for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'):
            fix_revert(os.path.join(root, f))
