CSV_PATH = r"D:\Simmiland.Build.7533614\Simmiland\simmiland_localization.csv"

with open(CSV_PATH, 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8-sig')
print(f"Original file size: {len(raw)} bytes")

# STEP 1: Typo fixes
mass_replacements = [
    ('используеться', 'используется'),
    ('добываеться', 'добывается'),
    ('получаеться', 'получается'),
    ('переплавляеться', 'переплавляется'),
    ('водросли', 'водоросли'),
    ('братарейка', 'батарейка'),
    ('производиться людьми', 'производится людьми'),
    ('лекврства', 'лекарства'),
    ('дрнвесный уголь', 'древесный уголь'),
    ('писменность', 'письменность'),
    ('джунгливое дерево', 'дерево джунглей'),
    ('меторождение глины', 'месторождение глины'),
    ('соломенная хижена', 'соломенная хижина'),
    ('заваод', 'завод'),
    ('землятрясение', 'землетрясение'),
    ('багословение', 'благословение'),
    ('класика', 'классика'),
    ('рзблокировать', 'разблокировать'),
    ('ракетостроени,,', 'ракетостроение,,'),
    ('маленьеий остров', 'маленький остров'),
    ('человечеств стало ближе к природе', 'природа человечества стала'),
]
for old, new in mass_replacements:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"  Fixed '{old}' -> '{new}' ({count}x)")

# Context-specific fixes
content = content.replace('menu_stars,stars,星星,星星,estrellas,,,,начать',
                          'menu_stars,stars,星星,星星,estrellas,,,,звёзды')
content = content.replace('game_manstate_name_building,building,建築,建筑,construyendo,,,,здание',
                          'game_manstate_name_building,building,建築,建筑,construyendo,,,,строительство')
content = content.replace('game_capped,capped,鎖定,锁定,al límite,,,,покрытый',
                          'game_capped,capped,鎖定,锁定,al límite,,,,ограничено')
content = content.replace('может быть уточнен', 'можно переплавить')
content = content.replace('game_feeds,feeds,飽食度,饱食度,alimenta,,,,корма',
                          'game_feeds,feeds,飽食度,饱食度,alimenta,,,,питательность')
content = content.replace('game_fertilized,fertilized,已施肥,已施肥,fertilizado,,,,оплодотворенный',
                          'game_fertilized,fertilized,已施肥,已施肥,fertilizado,,,,удобренная')
content = content.replace('game_unfertilized,unfertilized,未施肥,未施肥,no fertilizado,,,,неоплодотворенные',
                          'game_unfertilized,unfertilized,未施肥,未施肥,no fertilizado,,,,неудобренная')
content = content.replace('food_name_drumstick,drumstick,雞腿,鸡腿,muslo de pollo,,Keule,,голень',
                          'food_name_drumstick,drumstick,雞腿,鸡腿,muslo de pollo,,Keule,,куриная ножка')
content = content.replace('1 стакан в плавильной печи', '1 стекло в плавильной печи')
content = content.replace(
    'research_comp_info_currency,researched when playing inspect on gold#a little bit of IQ is needed#before mankind can research this##mankind sees value in gold and creates currency#that enables trade,研究金礦後習得#人類需要一點IQ#才能發明貨幣##人類看見了黃金的價值並將之作為貨幣#可以發展交易,研究黄金后习得#需要一点IQ#在人类研究此物前##人类发现了黄金的价值，创造了货币#使得贸易产生,investigado al usar examinar en oro#se necesita un poquito de inteligencia#antes de que la humanidad pueda investigar esto##la humanidad ve el valor en el oro y crea el dinero#que permite el comercio,,,,исследуется при игре в инспекцию плутония#требуется огромное количество IQ#прежде чем человечество сможет исследовать это##позволяет построить портал пространства-времени#ценой 5 плутония#создавая настоящий побег до их конца!',
    'research_comp_info_currency,researched when playing inspect on gold#a little bit of IQ is needed#before mankind can research this##mankind sees value in gold and creates currency#that enables trade,研究金礦後習得#人類需要一點IQ#才能發明貨幣##人類看見了黃金的價值並將之作為貨幣#可以發展交易,研究黄金后习得#需要一点IQ#在人类研究此物前##人类发现了黄金的价值，创造了货币#使得贸易产生,investigado al usar examinar en oro#se necesita un poquito de inteligencia#antes de que la humanidad pueda investigar esto##la humanidad ve el valor en el oro y crea el dinero#que permite el comercio,,,,исследуется при осмотре золота#требуется немного IQ#прежде чем человечество сможет это исследовать##человечество видит ценность в золоте и создаёт валюту#которая позволяет торговлю'
)
print("\nTypo fixes complete!")

# STEP 2: Copy Russian (col 8) -> Spanish (col 4)
def split_csv_fields(line):
    fields = []
    current = []
    in_quotes = False
    for ch in line:
        if ch == '"':
            in_quotes = not in_quotes
            current.append(ch)
        elif ch == ',' and not in_quotes:
            fields.append(''.join(current))
            current = []
        else:
            current.append(ch)
    fields.append(''.join(current))
    return fields

RUSSIAN_COL = 8
SPANISH_COL = 4

lines = content.split('\r\n')
new_lines = []
copied = 0

for idx, line in enumerate(lines):
    fields = split_csv_fields(line)
    if len(fields) > RUSSIAN_COL:
        russian = fields[RUSSIAN_COL].strip()
        if russian and russian != '0':
            fields[SPANISH_COL] = fields[RUSSIAN_COL]
            copied += 1
    new_lines.append(','.join(fields))

print(f"Copied Russian to Spanish column (col 4) for {copied} rows")

# STEP 3: Change display name español -> Русский
for idx, line in enumerate(new_lines):
    if line.startswith('language name,'):
        fields = split_csv_fields(line)
        if len(fields) > SPANISH_COL:
            print(f"Language row: col4 was '{fields[SPANISH_COL]}'")
            fields[SPANISH_COL] = 'Русский'
            new_lines[idx] = ','.join(fields)
            print(f"  -> Changed to 'Русский'")
        break

# STEP 4: Save
result = '\r\n'.join(new_lines)
result_bytes = result.encode('utf-8')
with open(CSV_PATH, 'wb') as f:
    f.write(result_bytes)
print(f"\nSaved! {len(result_bytes)} bytes, {len(new_lines)} lines")

# Verify
vlines = result.split('\r\n')
print(f"\nHeader: {vlines[0][:120]}")
for vl in vlines[:10]:
    if vl.startswith('language name'):
        print(f"Lang names: {vl[:120]}")
for vl in vlines[5:15]:
    f = split_csv_fields(vl)
    if len(f) > 4 and f[0].startswith('resource_name_t'):
        print(f"Sample: id='{f[0]}' spanish/ru='{f[4]}' russian='{f[8] if len(f)>8 else ''}'")
        break
