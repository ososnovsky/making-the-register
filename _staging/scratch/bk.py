"""python bk.py urls.txt : print snippets about group/private offers with prices"""
import sys,re,html
sys.path.insert(0,'.')
from verify import fetch
from concurrent.futures import ThreadPoolExecutor
KW=re.compile(r"(skupin|na objednávku|na objednavku|na požiadanie|rezervác|group|private|súkromn|workshop|degustác|komentovan|sprievodc|prehliadk|team.?building|firemn)",re.I)
def one(line):
    u=line.split(" | ")[-1].strip(); n=line.split(" | ")[0]
    st,fu,b=fetch(u)
    t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style|nav|footer).*?</\1>","",b))))
    sn=[]
    for m in KW.finditer(t):
        s=t[max(0,m.start()-70):m.end()+130]
        if re.search(r"€|eur|EUR",s) and s[:40] not in [x[:40] for x in sn]: sn.append(s)
        if len(sn)>=4: break
    return f"== {n} {u} [{st}]\n"+"\n".join("   - "+s for s in sn)
with ThreadPoolExecutor(12) as ex:
    for r in ex.map(one,[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip()]): print(r,flush=True)
