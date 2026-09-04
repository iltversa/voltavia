import base64, os, re, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'index.html')
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, 'illicium-motors-standalone.html')

html = open(src, encoding='utf-8').read()

MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml'}
cache = {}
missing = []

def repl(m):
    rel = m.group(1)
    if rel in cache:
        return 'src="%s"' % cache[rel]
    path = os.path.join(root, rel.replace('/', os.sep))
    if not os.path.exists(path):
        missing.append(rel)
        return m.group(0)
    ext = os.path.splitext(path)[1].lower()
    b64 = base64.b64encode(open(path, 'rb').read()).decode('ascii')
    uri = 'data:%s;base64,%s' % (MIME.get(ext, 'application/octet-stream'), b64)
    cache[rel] = uri
    return 'src="%s"' % uri

out = re.sub(r'src="(assets/[^"]+)"', repl, html)

# lazy-loading is pointless once inlined, and it delays paint on some engines
out = out.replace(' loading="lazy"', '')

open(dst, 'w', encoding='utf-8').write(out)
print('inlined %d unique images' % len(cache))
if missing:
    print('MISSING:', missing)
print('output %.2f MB' % (os.path.getsize(dst) / 1048576))
