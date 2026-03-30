import re

files = [
    "/Users/leanazorzetto/Desktop/site web/A2CI-astro/formations-incendie.html",
    "/Users/leanazorzetto/Desktop/site web/A2CI-astro/formations-secourisme.html"
]

# The regex will target the exact block:
# <div class="grid grid-cols-2 gap-[23]">
#   <a href="formation-xxx.html" class="...">En savoir plus</a>
#   ... anything until </div> of the gap-3 block
# </div>

pattern = re.compile(
    r'<div class="grid grid-cols-2 gap-3">\s*'
    r'<a href="([^"]+)"\s*class="[^"]*">En savoir plus</a>\s*'
    r'(?:<a [^>]+>.*?</a>|<div class="grid grid-cols-2 gap-2">.*?</div>)\s*'
    r'</div>',
    re.DOTALL
)

for filepath in files:
    with open(filepath, "r") as f:
        content = f.read()

    # We replace it with a single full-width gray button
    def replacer(match):
        href = match.group(1)
        return (f'<a href="{href}" class="block w-full py-4 bg-gray-100 text-gray-900 '
                f'text-center rounded-xl hover:bg-gray-200 transition-all '
                f'text-[10px] font-bold uppercase tracking-widest border border-gray-200">'
                f'En savoir plus</a>')

    new_content, count = pattern.subn(replacer, content)
    
    if count > 0:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Replaced {count} instances in {filepath}")
    else:
        print(f"No instances found in {filepath} or regex failed")
