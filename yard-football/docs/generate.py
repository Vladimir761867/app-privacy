"""Render static privacy/support pages from each product's localized source."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT/'docs/content.json').read_text(encoding='utf-8'))
PRODUCT = json.loads((ROOT/'docs/product.json').read_text(encoding='utf-8'))
EMAIL = PRODUCT['email']
DEVELOPERS = ', '.join(PRODUCT['developers'])
CONTROLLERS = PRODUCT['dataController'] if isinstance(PRODUCT['dataController'], list) else [PRODUCT['dataController']]
CONTROLLER = ', '.join(CONTROLLERS)
assert DEVELOPERS and CONTROLLER

def render(kind):
    articles = []
    for code in [k for k in DATA if k != 'en'] + ['en']:
        d = DATA[code]
        brand = d.get('brand',PRODUCT['name'])
        language_links = ''.join(
            f'<a href="#{k}" lang="{k}" hreflang="{k}"'
            + (' aria-current="true"' if k == code else '')
            + f'>{escape(v["name"])}</a>' for k,v in DATA.items()
        )
        navigation = ''.join(
            f'<a href="{page}.html#{code}"'
            + (' aria-current="page"' if page == kind else '')
            + f'>{escape(d[page])}</a>' for page in ['privacy','support']
        )
        pairs = d['sections'] if kind == 'privacy' else d['faq']
        sections = ''.join(f'<section><h2>{escape(h)}</h2><p>{escape(p)}</p></section>\n' for h,p in pairs)
        intro = d['intro'] if kind == 'privacy' else d['supportIntro']
        articles.append(f'''<article class="document" id="{code}" lang="{code}" aria-labelledby="title-{code}">
<header>
<p class="brand">{escape(brand)}</p>
<p class="date"><time datetime="2026-11-27">{escape(d['date'])}</time></p>
<nav class="languages" aria-label="{escape(d['language'])}">{language_links}</nav>
<nav class="pages" aria-label="{escape(brand)}">{navigation}</nav>
<h1 id="title-{code}">{escape(d[kind])}</h1>
<p class="intro">{escape(intro)}</p>
<p>{escape(d['developersLabel'])}: {escape(DEVELOPERS)}.</p>
<p>{escape(d['controllerLabel'])}: {escape(CONTROLLER)}.</p>
</header>
<aside class="contact" aria-label="{escape(d['contact'])}"><span>{escape(d['contact'])}</span><a href="mailto:{EMAIL}">{EMAIL}</a></aside>
{sections}
<footer><a href="{'support' if kind == 'privacy' else 'privacy'}.html#{code}">{escape(d['support' if kind == 'privacy' else 'privacy'])}</a><span>{escape(brand)} · {escape(DEVELOPERS)}</span></footer>
</article>''')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; base-uri 'none'; form-action 'none'">
<title>{escape(DATA['en'][kind])} — {escape(PRODUCT['name'])}</title>
<meta name="description" content="{escape(DATA['en'][kind])} for {escape(PRODUCT['name'])}. Developers: {escape(DEVELOPERS)}. Data controller{'s' if len(CONTROLLERS) > 1 else ''}: {escape(CONTROLLER)}. Contact: {EMAIL}.">
<link rel="stylesheet" href="style.css">
</head>
<body><main>
{''.join(articles)}
</main></body>
</html>
'''

for page in ['privacy','support']:
    (ROOT/f'{page}.html').write_text(render(page),encoding='utf-8',newline='\n')
print(PRODUCT['name']+': generated six-language privacy and support; no JavaScript.')
