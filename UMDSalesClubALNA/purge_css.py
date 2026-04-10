import os
import re
import cssutils
import logging
from bs4 import BeautifulSoup

cssutils.log.setLevel(logging.CRITICAL)

html_classes = set()
html_ids = set()
html_tags = set()

# Whitelist everything
dynamic_classes = {
    'is-preload', 'is-mobile', 'navPanel-visible', 'dropotron', 'active', 'alt', 'toggle', 
    'locked', 'reveal', 'landing', 'bg', 'wrapper', 'nav', 'title', 'navButton', 'inner',
    'major', 'special', 'features', 'scrolly', 'scrollex', 'container', 'row', 'col-6', 'col-12-narrower', 'col-12-mobilep', 'col-4', 'col-12-mobile', 'col-5', 'col-7', 'col-8', 'button', 'primary', 'icon', 'solid', 'brands', 'image', 'featured', 'fit', 'left', 'right'
}
dynamic_ids = {'navPanel', 'page-wrapper', 'titleBar'}
dynamic_tags = {'html', 'body', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'br', 'hr', 'ul', 'ol', 'li', 'header', 'footer', 'section', 'nav', 'i', 'b', 'strong', 'em', 'iframe', 'main', 'script', 'style', 'head', 'title', 'meta', 'link'}

html_classes.update(dynamic_classes)
html_ids.update(dynamic_ids)
html_tags.update(dynamic_tags)

for root, _, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root or 'assets' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                for tag in soup.find_all(True):
                    html_tags.add(tag.name.lower())
                    if tag.get('class'):
                        html_classes.update(tag.get('class'))
                    if tag.get('id'):
                        html_ids.add(tag.get('id'))

js_re = re.compile(r'\.(addClass|removeClass|toggleClass)\([\'"]([a-zA-Z0-9_-]+)[\'"]\)')
for root, _, files in os.walk('assets/js'):
    for file in files:
        if file.endswith('.js'):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                matches = js_re.findall(content)
                for m in matches:
                    html_classes.add(m[1])

css_path = 'assets/css/main.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Backup
with open('assets/css/main_backup.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

sheet = cssutils.parseString(css_content)

def selector_is_used(sel):
    sel = sel.strip()
    if not sel: return False
    sel = re.sub(r'::?[a-zA-Z0-9_-]+(\([^)]*\))?', '', sel)
    sel = re.sub(r'\[[^\]]+\]', '', sel)
    parts = re.split(r'[ \t>+~]+', sel)
    
    for part in parts:
        if not part: continue
        tokens = re.split(r'([.#][a-zA-Z0-9_\-]+)', part)
        first_tok = tokens[0].lower()
        if first_tok and first_tok not in html_tags and first_tok != '*' and first_tok != 'page':
            return False
            
        for t in tokens[1:]:
            if not t: continue
            if t.startswith('.'):
                c = t[1:]
                if c not in html_classes: return False
            elif t.startswith('#'):
                i = t[1:]
                if i not in html_ids: return False
    return True

rules_dropped = 0

for i in range(len(sheet.cssRules) - 1, -1, -1):
    rule = sheet.cssRules[i]
    if rule.type == rule.STYLE_RULE:
        valid = []
        for s in rule.selectorList:
            if selector_is_used(s.selectorText):
                valid.append(s.selectorText)
        if valid:
            if len(valid) != len(rule.selectorList):
                rule.selectorText = ', '.join(valid)
        else:
            sheet.deleteRule(i)
            rules_dropped += 1
            
    elif rule.type == rule.MEDIA_RULE:
        inner_dropped = 0
        for j in range(len(rule.cssRules) - 1, -1, -1):
            inner_rule = rule.cssRules[j]
            if inner_rule.type == inner_rule.STYLE_RULE:
                valid = []
                for s in inner_rule.selectorList:
                    if selector_is_used(s.selectorText):
                        valid.append(s.selectorText)
                if valid:
                    if len(valid) != len(inner_rule.selectorList):
                        inner_rule.selectorText = ', '.join(valid)
                else:
                    rule.deleteRule(j)
                    inner_dropped += 1
        if len(rule.cssRules) == 0:
            sheet.deleteRule(i)
            rules_dropped += 1

print(f"Dropped {rules_dropped} styles.")

with open(css_path, 'wb') as f:
    f.write(sheet.cssText)
