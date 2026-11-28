# Source for privacy.html and support.html

- `content.json` — all page text, one entry per language.
- `product.json` — game name, developers, data controllers and contact email.
- `generate.py` — builds `../privacy.html` and `../support.html`.

After editing, run from the repository root:

```bash
python3 afterburn-skies/docs/generate.py
```

The pages need no JavaScript: language switching uses `#language` links and CSS. Everything is local — no analytics, cookies, fonts or external scripts.
