import sys,re,html
sys.path.insert(0,'.')
from verify import fetch
u=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 1200
pat=sys.argv[3] if len(sys.argv)>3 else None
st,fu,b=fetch(u)
b2=re.sub(r"(?s)<(script|style|svg|noscript).*?</\1>","",b)
t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",b2)))
print(st,fu,len(b))
if pat:
    for m in list(re.finditer(pat,b,re.I))[:12]:
        print("...",re.sub(r"\s+"," ",b[max(0,m.start()-100):m.end()+160]))
else: print(t[:n])
