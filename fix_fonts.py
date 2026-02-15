import os

target_dir = r"c:\Users\Om\Documents\KrackHack Hackathon\frontend\src"
print(f"Scanning {target_dir}...")

count = 0
for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".tsx"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content.replace("font-black", "font-bold")
            new_content = new_content.replace("font-extrabold", "font-bold")
            
            if new_content != content:
                print(f"Updating {path}")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1

print(f"Updated {count} files.")
