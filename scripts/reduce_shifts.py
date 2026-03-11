"""Reduce Cyrillic shifts by 3px in all _cyr.csv files."""
import os, glob

FONTS_DIR = r"D:\Simmiland.Build.7533614\Simmiland\cyrillic_fonts"
REDUCE = 3

for csv_path in sorted(glob.glob(os.path.join(FONTS_DIR, "glyphs_*_cyr.csv"))):
    with open(csv_path, 'r') as f:
        lines = f.readlines()
    
    new_lines = [lines[0]]
    adj = 0
    for line in lines[1:]:
        parts = line.strip().split(';')
        if len(parts) >= 7:
            ch = int(parts[0])
            if 0x0400 <= ch <= 0x04FF:
                shift = int(parts[5])
                parts[5] = str(max(shift - REDUCE, 2))
                adj += 1
                new_lines.append(';'.join(parts) + '\n')
                continue
        new_lines.append(line)
    
    with open(csv_path, 'w') as f:
        f.writelines(new_lines)
    
    fn = os.path.basename(csv_path).replace('glyphs_','').replace('_cyr.csv','')
    print(f"  {fn}: {adj} glyphs -3px")

print("Done!")
