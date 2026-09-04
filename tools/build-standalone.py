import base64, os, re, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'index.html')
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, 'voltavia-standalone.html')

html = open(src, encoding='utf-8').read()

MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.svg': 'image/svg+xml', '.mp4': 'video/mp4'}
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

def to_uri(rel):
    path = os.path.join(root, rel.replace('/', os.sep))
    if not os.path.exists(path):
        missing.append(rel)
        return None
    ext = os.path.splitext(path)[1].lower()
    b64 = base64.b64encode(open(path, 'rb').read()).decode('ascii')
    return 'data:%s;base64,%s' % (MIME.get(ext, 'application/octet-stream'), b64)

out = re.sub(r'src="(assets/[^"]+)"', repl, html)

# the scrub video and its poster are referenced from JS, not from a src attribute.
# The page checks for a data: prefix and skips the blob fetch when it finds one.
for var in ('ANATOMY_URL', 'ANATOMY_POSTER'):
    m = re.search(r"var %s='(assets/[^']+)';" % var, out)
    if m:
        uri = to_uri(m.group(1))
        if uri:
            out = out.replace(m.group(0), "var %s='%s';" % (var, uri), 1)
            cache[m.group(1)] = uri

# lazy-loading is pointless once inlined, and it delays paint on some engines
out = out.replace(' loading="lazy"', '')

open(dst, 'w', encoding='utf-8').write(out)
print('inlined %d unique images' % len(cache))
if missing:
    print('MISSING:', missing)
print('output %.2f MB' % (os.path.getsize(dst) / 1048576))
