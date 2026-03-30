import re
import os

files = [
    'formations-secourisme.html',
    'formations-incendie.html'
]

def replace_match(m):
    href = m.group(1)
    return f'<a href="{href}" class="w-full py-4 bg-gray-200 text-gray-500 text-center rounded-xl hover:bg-gray-300 hover:text-gray-900 transition-all text-[10px] font-bold uppercase tracking-widest shadow-sm block border border-gray-300">En savoir plus</a>'

patt1 = re.compile(r'<div class="grid grid-cols-2 gap-3">\s*<a href="([^"]+)"[^>]+>En savoir plus</a>\s*<a href="[^"]+"[^>]+>Fiche \(PDF\)</a>\s*</div>')
patt2 = re.compile(r'<div class="grid grid-cols-2 gap-3">\s*<a href="([^"]+)"[^>]+>En savoir plus</a>\s*<div class="grid grid-cols-2 gap-2">\s*<a href="[^"]+"[^>]+>Fiche 1</a>\s*<a href="[^"]+"[^>]+>Fiche 2</a>\s*</div>\s*</div>')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()

    original_length = len(text)
    text, n1 = patt1.subn(replace_match, text)
    text, n2 = patt2.subn(replace_match, text)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Replaced {n1 + n2} occurrences in {file} (standard: {n1}, complex: {n2})")
