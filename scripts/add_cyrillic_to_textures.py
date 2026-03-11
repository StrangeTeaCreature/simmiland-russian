"""
v10: Full-size chars, correct padding, NO shift reduction.
Clean version without any compression hacks.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS_DIR = r"D:\Simmiland.Build.7533614\Simmiland\cyrillic_fonts"
CYRILLIC = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяЁё"

TARGET_FONTS = [
    "font12", "fontm5x7", "fontm5x7x2",
    "fontwaku12", "fontwaku16", "fontwaku24", "fontwaku32", "fontwaku40",
    "fnt_bigwaku",
    "fontarial10", "fontarial12", "fontarial16", "fontarial20", "fontarial24", "fontarial32", "fontarial40",
    "fontCJK_10", "fontCJK_12", "fontCJK_16", "fontCJK_20", "fontCJK_24", "fontCJK_32", "fontCJK_40",
    "fontlana8", "fontlana8x2",
]

def next_pow2(v):
    p = 1
    while p < v:
        p *= 2
    return p

def measure_top_pad(img, x, y, w, h):
    for row in range(h):
        for col in range(w):
            if x + col < img.width and y + row < img.height:
                if img.getpixel((x + col, y + row))[3] > 0:
                    return row
    return 0

for font_name in TARGET_FONTS:
    png_path = os.path.join(FONTS_DIR, f"{font_name}.png")
    csv_path = os.path.join(FONTS_DIR, f"glyphs_{font_name}.csv")
    if not os.path.exists(png_path) or not os.path.exists(csv_path):
        continue
    
    orig_img = Image.open(png_path).convert("RGBA")
    orig_w, orig_h = orig_img.size
    
    with open(csv_path, 'r') as f:
        lines = f.readlines()
    
    existing_glyphs = []
    for line in lines[1:]:
        parts = line.strip().split(';')
        if len(parts) >= 7:
            existing_glyphs.append({
                'char': int(parts[0]), 'x': int(parts[1]), 'y': int(parts[2]),
                'w': int(parts[3]), 'h': int(parts[4]),
                'shift': int(parts[5]), 'offset': int(parts[6]),
            })
    if not existing_glyphs:
        continue
    
    heights = [g['h'] for g in existing_glyphs if g['h'] > 0]
    standard_h = max(set(heights), key=heights.count)
    offsets_list = [g['offset'] for g in existing_glyphs]
    standard_offset = max(set(offsets_list), key=offsets_list.count)
    
    ref_A = next((g for g in existing_glyphs if g['char'] == ord('A')), existing_glyphs[0])
    ref_a = next((g for g in existing_glyphs if g['char'] == ord('a')), ref_A)
    shift_A = ref_A['shift']
    shift_a = ref_a['shift']
    
    upper_shifts = set(g['shift'] for g in existing_glyphs if 65 <= g['char'] <= 90)
    is_mono = len(upper_shifts) <= 2
    
    top_pad_A = measure_top_pad(orig_img, ref_A['x'], ref_A['y'], ref_A['w'], ref_A['h'])
    top_pad_a = measure_top_pad(orig_img, ref_a['x'], ref_a['y'], ref_a['w'], ref_a['h'])
    
    font_path = "C:\\Windows\\Fonts\\consola.ttf"
    try:
        ImageFont.truetype(font_path, 10)
    except:
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
    
    available_h = standard_h - top_pad_A
    best_size = max(available_h - 2, 4)
    for test_size in range(available_h + 5, 3, -1):
        test_font = ImageFont.truetype(font_path, test_size)
        fits = True
        for ch in "ЩДБЙ":
            tmp = Image.new("RGBA", (test_size * 2, available_h * 2), (0, 0, 0, 0))
            ImageDraw.Draw(tmp).text((0, 0), ch, font=test_font, fill=(255,255,255,255))
            bb = tmp.getbbox()
            if bb and (bb[3] - bb[1]) > available_h:
                fits = False
                break
        if fits:
            best_size = test_size
            break
    
    render_font = ImageFont.truetype(font_path, best_size)
    
    cell_w = max(shift_A, shift_a) + 4
    cell_h = standard_h
    cols = max(1, orig_w // cell_w)
    needed_rows = (len(CYRILLIC) + cols - 1) // cols
    
    new_h = next_pow2(orig_h + needed_rows * cell_h + 4)
    new_w = next_pow2(orig_w)
    
    new_img = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    new_img.paste(orig_img, (0, 0))
    
    y_start = orig_h + 2
    new_glyphs = []
    
    for i, ch in enumerate(CYRILLIC):
        col = i % cols
        row = i // cols
        cell_x = col * cell_w
        cell_y = y_start + row * cell_h
        
        is_upper = (0x0410 <= ord(ch) <= 0x042F) or ord(ch) == 0x0401
        top_pad = top_pad_A if is_upper else top_pad_a
        
        big_buf = Image.new("RGBA", (cell_w + 10, standard_h * 2), (0, 0, 0, 0))
        ImageDraw.Draw(big_buf).text((0, 0), ch, font=render_font, fill=(255, 255, 255, 255))
        bb = big_buf.getbbox()
        
        cell_buf = Image.new("RGBA", (cell_w, standard_h), (0, 0, 0, 0))
        if bb:
            content = big_buf.crop((bb[0], bb[1], bb[2], min(bb[3], bb[1] + standard_h - top_pad)))
            cell_buf.paste(content, (0, top_pad))
            actual_w = bb[2] - bb[0]
        else:
            actual_w = shift_A
        
        new_img.paste(cell_buf, (cell_x, cell_y))
        
        # ORIGINAL shifts — no reduction!
        char_shift = shift_A if is_upper else shift_a
        
        new_glyphs.append({
            'char': ord(ch),
            'x': cell_x,
            'y': cell_y,
            'w': actual_w,
            'h': standard_h,
            'shift': char_shift,
            'offset': standard_offset,
        })
    
    out_png = os.path.join(FONTS_DIR, f"{font_name}_cyr.png")
    new_img.save(out_png)
    
    out_csv = os.path.join(FONTS_DIR, f"glyphs_{font_name}_cyr.csv")
    with open(out_csv, 'w') as f:
        f.write(lines[0])
        for line in lines[1:]:
            f.write(line)
        for g in new_glyphs:
            f.write(f"{g['char']};{g['x']};{g['y']};{g['w']};{g['h']};{g['shift']};{g['offset']}\n")
    
    print(f"  {font_name}: shift={shift_A}/{shift_a} (ORIGINAL) render={best_size}px pad={top_pad_A}/{top_pad_a}")

print("\nDone!")
