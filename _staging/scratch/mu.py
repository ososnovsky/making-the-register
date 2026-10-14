import sys,re,html,json
sys.path.insert(0,'.')
from verify import fetch
skip={'about','apps','blog','cities','find','login','lp','meetup-pro','register','sitemap','start','topics','vienna','budapest','prague','brno','sk','privacy','terms','help','careers','events','groups','pro','jobs','press','mobile','safety'}
slugs=set()
for t in ["","language-exchange","outdoor-activities","book-clubs","networking"]:
    st,fu,b=fetch("https://www.meetup.com/find/sk--bratislava/"+(t+"/" if t else ""))
    slugs|=set(re.findall(r'https://www\.meetup\.com/([A-Za-z0-9_%-]{3,60})/',b))
slugs-=skip
print(sorted(slugs))
for s in sorted(slugs):
    st,fu,b=fetch(f"https://www.meetup.com/{s}/")
    t=re.search(r"<title>(.*?)</title>",b)
    print(s,st,(html.unescape(t.group(1)) if t else '')[:80],flush=True)
