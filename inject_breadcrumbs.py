import os
import glob
import re

# Precise mapping of all pages to their breadcrumb hierarchy
# Format: { 'filename.html': [('Name', 'link.html'), ('Current Page', None)] }
hierarchy_map = {
    # Agence
    'a2ci.html': [("L'Agence", None)],
    
    # Securite Incendie
    'coordination-ssi.html': [("Sécurité Incendie", None), ("Coordination SSI", None)],
    'audit.html': [("Sécurité Incendie", None), ("Audit & Conseil", None)],
    'bet-amo.html': [("Sécurité Incendie", None), ("BET & AMO", None)],
    'aide-exploitant.html': [("Sécurité Incendie", None), ("Aide à l'Exploitant", None)],
    
    # Hygiene & Securite
    'document-unique.html': [("Hygiène & Sécurité", None), ("Document Unique (D.U)", None)],
    'ppms.html': [("Hygiène & Sécurité", None), ("PPMS", None)],
    'notices.html': [("Hygiène & Sécurité", None), ("Notices", None)],
    
    # Formations Main
    'formations.html': [("Formations", None)],
    'inscriptions-formations.html': [("Formations", "formations.html"), ("Modalités d'inscription", None)],
    'certifications-satisfaction.html': [("Formations", "formations.html"), ("Satisfaction & Certification", None)],
    
    # Formations Catalogues
    'formations-incendie.html': [("Formations", "formations.html"), ("Formations INCENDIE", None)],
    'formations-secourisme.html': [("Formations", "formations.html"), ("Formations SECOURISME", None)],
    
    # Blog
    'blog.html': [("Blog", None)],
    
    # Types de bâtiments
    'erp.html': [("Type de bâtiments", "index.html#secteurs"), ("ERP", None)],
    'igh.html': [("Type de bâtiments", "index.html#secteurs"), ("IGH", None)],
    'industries.html': [("Type de bâtiments", "index.html#secteurs"), ("Industries", None)],
    'habitation.html': [("Type de bâtiments", "index.html#secteurs"), ("Habitation", None)],
    'sante-soins.html': [("Type de bâtiments", "index.html#secteurs"), ("Établissements de Soins", None)],
    'sieges-sociaux.html': [("Type de bâtiments", "index.html#secteurs"), ("Sièges Sociaux", None)],
    'tertiaire-ert.html': [("Type de bâtiments", "index.html#secteurs"), ("Code du Travail / ERT", None)],
    'culture-loisirs.html': [("Type de bâtiments", "index.html#secteurs"), ("Établissements Culturels & Loisirs", None)],
}

formations_incendie_pages = {
    'formation-ari.html': "Port de l'ARI",
    'formation-ari-recyclage.html': "Maintien des Acquis ARI",
    'formation-epi.html': "Équipier de Première Intervention (EPI)",
    'formation-esi.html': "Équipier de Seconde Intervention (ESI)",
    'formation-evacuation-gsf.html': "Guides & Serre-Files (GSF)",
    'formation-exercice-evacuation.html': "Exercice d’Évacuation",
    'formation-referent-incendie.html': "Référent Incendie Site",
    'formation-ria.html': "Manipulation des R.I.A",
    'formation-sri.html': "Sensibilisation au Risque Incendie (SRI)",
    'formation-sri-handicap.html': "Risque Incendie (Handicap)",
    'formation-ssi.html': "Exploitation du SSI",
    'formation-transfert-horizontal.html': "Transfert Horizontal (Type U/J)",
}

formations_secourisme_pages = {
    'formation-sst.html': "Sauveteur Secouriste du Travail (SST)",
    'formation-dae.html': "Initiation au Défibrillateur (DAE)",
    'formation-mac-sst.html': "Maintien et Actualisation des Compétences (MAC SST)",
    'formation-ps.html': "Sensibilisation aux Premiers Secours",
}

for page, name in formations_incendie_pages.items():
    hierarchy_map[page] = [("Formations", "formations.html"), ("Formations INCENDIE", "formations-incendie.html"), (name, None)]

for page, name in formations_secourisme_pages.items():
    hierarchy_map[page] = [("Formations", "formations.html"), ("Formations SECOURISME", "formations-secourisme.html"), (name, None)]

def generate_breadcrumb_html(path_list):
    html = '''
<nav aria-label="Breadcrumb" class="bg-gray-50 border-b border-gray-200 py-3 px-8 text-xs font-medium text-gray-500 w-full z-20 relative">
  <div class="max-w-[1440px] mx-auto flex items-center gap-2 overflow-x-auto whitespace-nowrap scrollbar-hide">
    <a href="index.html" class="hover:text-[var(--a2ci-red)] transition-colors inline-flex items-center gap-1">
      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
      Accueil
    </a>'''
    
    for i, (name, link) in enumerate(path_list):
        html += '\n    <span class="text-gray-300">/</span>'
        if link:
            html += f'\n    <a href="{link}" class="hover:text-[var(--a2ci-red)] transition-colors">{name}</a>'
        else:
            if i == len(path_list) - 1:
                html += f'\n    <span class="text-gray-900 font-bold" aria-current="page">{name}</span>'
            else:
                html += f'\n    <span class="text-gray-500">{name}</span>'
                
    html += '\n  </div>\n</nav>'
    return html

html_files = glob.glob('*.html')
success_count = 0
not_mapped = []

# Pattern to find header-component and inject right below it
header_pattern = re.compile(r'(<div id="header-component"></div>)', re.IGNORECASE)

for file in html_files:
    if file == 'index.html':
        continue
        
    path_list = hierarchy_map.get(file)
    if not path_list:
        not_mapped.append(file)
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if already has breadcrumb
    if 'aria-label="Breadcrumb"' in content:
        print(f"[{file}] Breadcrumb already exists.")
        continue
        
    # Generate HTML
    breadcrumb_html = generate_breadcrumb_html(path_list)
    
    # Insert safely below header
    if header_pattern.search(content):
        new_content = header_pattern.sub(r'\1\n' + breadcrumb_html, content, count=1)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        success_count += 1
        print(f"[{file}] -> Added breadcrumb.")
    else:
        print(f"[{file}] ERROR: Couldn't find <div id=\"header-component\"></div>")

print(f"\nSuccessfully added breadcrumbs to {success_count} files.")
if not_mapped:
    print(f"Warning: these files have no mappings defined: {not_mapped}")
