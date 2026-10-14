import sys,re
sys.path.insert(0,'.')
from verify import fetch
from concurrent.futures import ThreadPoolExecutor
def f(u):
    st,fu,b=fetch(u)
    t=re.search(r"<title[^>]*>(.*?)</title>",b,re.S|re.I)
    t=re.sub(r"\s+"," ",t.group(1)).strip()[:80] if t else ""
    return f"{st} {u} -> {fu if fu!=u else ''} [{t}] len={len(b)}"
urls=[l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
with ThreadPoolExecutor(20) as ex:
    for r in ex.map(f,urls): print(r)
