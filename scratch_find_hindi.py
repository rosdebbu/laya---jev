import re
import os

base_dir = r"c:\Users\ROSHNI\OneDrive\Documents\GitHub\laya---jev"

for fname in ["web/index.html", "web/app.js"]:
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    hindi_lines = []
    for i, line in enumerate(lines):
        if re.search(r"[\u0900-\u097F]", line):
            hindi_lines.append((i + 1, line.strip()))
    safe_name = fname.replace("/", "_").replace("\\", "_")
    out_path = os.path.join(base_dir, f"scratch_{safe_name}_hindi.txt")
    with open(out_path, "w", encoding="utf-8") as out:
        for num, text in hindi_lines:
            out.write(f"L{num}: {text}\n")
    print(f"{fname}: {len(hindi_lines)} lines written to {out_path}")
print("Done.")
