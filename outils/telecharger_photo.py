"""Télécharge les photos choisies. Usage : python3 telecharger_photo.py nom=slug:index ... -> sel/nom.jpg + sel/credits.json"""
import json, sys, time, pathlib
from chercher_photo import get, KEYS, BASE

sel = BASE / 'sel'
sel.mkdir(exist_ok=True)
meta_path = sel / 'credits.json'
meta = json.load(open(meta_path)) if meta_path.exists() else {}
for arg in sys.argv[1:]:
    name, rest = arg.split('=')
    slug, idx = rest.rsplit(':', 1)
    c = json.load(open(BASE / 'cand' / slug / 'cand.json'))[int(idx)]
    try:
        data = get(c['full'])
    except Exception as e:
        print('FAIL', name, e)
        continue
    (sel / f'{name}.jpg').write_bytes(data)
    if c['source'] == 'unsplash':
        get(c['download_location'], {'Authorization': 'Client-ID ' + KEYS['UNSPLASH_ACCESS_KEY']})
    meta[name] = dict(source=c['source'], author=c['author'], license=c['license'], page=c['page'], title=c['title'])
    print('ok', name, len(data), c['author'], c['license'])
    time.sleep(3)
json.dump(meta, open(meta_path, 'w'), ensure_ascii=False, indent=1)
