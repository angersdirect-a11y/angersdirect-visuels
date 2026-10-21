"""Recherche de photos. Usage : UNSPLASH_ACCESS_KEY=... python3 chercher_photo.py wm|us "requête" [n]
wm = Wikimedia Commons (lieux réels, vérifier la licence), us = Unsplash (illustration).
Écrit les candidats dans cand/<slug>/cand.json et des vignettes à regarder avant de choisir."""
import json, os, re, sys, urllib.parse, urllib.request, pathlib

BASE = pathlib.Path(__file__).parent
UA = 'AngersDirectBot/1.0 (redaction@angersdirect.fr)'
KEYS = {'UNSPLASH_ACCESS_KEY': os.environ.get('UNSPLASH_ACCESS_KEY', '')}


def get(url, headers=None, tries=6):
    import time, urllib.error
    for t in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': UA, **(headers or {})})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or t == tries - 1:
                raise
            time.sleep(4 * (t + 1))


def strip(html):
    return re.sub(r'<[^>]+>', '', html or '').strip()


def wikimedia(q, n):
    params = dict(action='query', format='json', generator='search', gsrnamespace=6, gsrsearch=q, gsrlimit=n,
                  prop='imageinfo', iiprop='url|size|extmetadata|mime', iiurlwidth=1280)
    data = json.loads(get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)))
    out = []
    for p in sorted(data.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 0)):
        ii = p['imageinfo'][0]
        if ii.get('mime') not in ('image/jpeg', 'image/png') or ii['width'] < ii['height']:
            continue
        m = ii.get('extmetadata', {})
        out.append(dict(source='wikimedia', title=p['title'], page=ii['descriptionurl'], thumb=ii['thumburl'].replace('thumb.wikimedia.org', 'upload.wikimedia.org').split('?')[0],
                        full=ii['thumburl'].replace('thumb.wikimedia.org', 'upload.wikimedia.org').split('?')[0], w=ii['width'], h=ii['height'],
                        author=strip(m.get('Artist', {}).get('value')), license=m.get('LicenseShortName', {}).get('value', '')))
    return out


def unsplash(q, n):
    url = 'https://api.unsplash.com/search/photos?' + urllib.parse.urlencode(dict(query=q, per_page=n, orientation='landscape', content_filter='high'))
    data = json.loads(get(url, {'Authorization': 'Client-ID ' + KEYS['UNSPLASH_ACCESS_KEY']}))
    return [dict(source='unsplash', title=r.get('alt_description') or r.get('description') or '', page=r['links']['html'],
                 thumb=r['urls']['small'], full=r['urls']['raw'] + '&w=1600&q=85&fm=jpg', download_location=r['links']['download_location'],
                 w=r['width'], h=r['height'], author=r['user']['name'], license='Unsplash License') for r in data['results']]


if __name__ == '__main__':
    src, q = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    res = (wikimedia if src == 'wm' else unsplash)(q, n)
    slug = re.sub(r'[^a-z0-9]+', '-', (src + '-' + q).lower()).strip('-')
    d = BASE / 'cand' / slug
    d.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(res):
        try:
            import time; time.sleep(1.5)
            (d / f'{i}.jpg').write_bytes(get(r['thumb']))
        except Exception as e:
            print('thumb fail', i, e)
    json.dump(res, open(d / 'cand.json', 'w'), ensure_ascii=False, indent=1)
    for i, r in enumerate(res):
        print(i, r['w'], 'x', r['h'], '|', r['license'], '|', r['author'][:40], '|', r['title'][:70])
    print('DIR', d)
