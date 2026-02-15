import os
import re

target_dir = r"c:\Users\Om\Documents\KrackHack Hackathon\frontend\src"
print(f"Scanning {target_dir}...")

def replace_font_sizes(content):
    # Standardize H1/Text sizes to text-2xl
    # Matches text-3xl, 4xl, 5xl followed by text-slate-900 (typical for headers)
    content = re.sub(r'(text-[345]xl)(?=.*text-slate-900)', 'text-2xl', content)
    
    # Standardize Icons
    # text-6xl -> text-5xl (Massive icons -> Large)
    content = re.sub(r'(material-symbols-outlined.*?)text-6xl', r'\1text-5xl', content)
    # text-5xl -> text-4xl
    content = re.sub(r'(material-symbols-outlined.*?)text-5xl', r'\1text-4xl', content)
    # text-4xl -> text-3xl
    content = re.sub(r'(material-symbols-outlined.*?)text-4xl', r'\1text-3xl', content)
    
    # Specific fix for "text-5xl" headers that might have been missed if not followed immediately by text-slate-900 in the regex lookahead buffer
    # But the above lookahead should work for "text-4xl font-bold text-slate-900"
    
    return content

count = 0
for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".tsx"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = replace_font_sizes(content)
            
            if new_content != content:
                print(f"Updating {path}")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1

print(f"Updated {count} files.")
