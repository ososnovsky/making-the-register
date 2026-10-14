"""Resolve names to candidate official sites via DuckDuckGo HTML. Usage: python find.py names.txt  (one name per line; ' @ extra' appended to query)"""
import sys,re,html,time,urllib.request,urllib.parse
from concurrent.futures import ThreadPoolExecutor
SKIP=re.compile(r"wikipedia|tripadvisor|facebook|instagram|yelp|trek\.zone|travelunify|wanderlog|foursquare|youtube|booking\.com|getyourguide|viator|mapcarta|google\.|restaurantguru|zoznam\.sk/firma|firmy\.|azet|linkedin|twitter|x\.com|pinterest|tiktok|expedia|kayak|hotels|airbnb|europages|cylex|mapy\.cz|openstreetmap|findglocal|waze|2gis|top-rated|slovakia\.travel|lonelyplanet|timeout|visitbratislava|bratislava\.sk|inyourpocket|eventbrite|goout|ticketportal|ra\.co|zlatestranky|nicelocal",re.I)
def ddg(q):
    u="https://html.duckduckgo.com/html/?q="+urllib.parse.quote(q)
    for _ in range(3):
        try:
            r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
            b=urllib.request.urlopen(r,timeout=20).read().decode("utf-8","replace")
            return [(html.unescape(re.sub('<[^>]+>','',t)).strip()[:60],urllib.parse.unquote(re.sub(r'.*uddg=([^&]+).*',r'\1',h))) for h,t in re.findall(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>',b)]
        except Exception as e:
            time.sleep(4)
    return []
def one(n):
    time.sleep(6)
    q=n if "@" not in n else n.replace("@","")
    res=[x for x in ddg(q+(" Bratislava" if "Bratislava" not in q else "")) if not SKIP.search(x[1])][:3]
    return f"{n}\n"+"\n".join(f"     {t} | {u}" for t,u in res)
names=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip() and not l.startswith("#")]
with ThreadPoolExecutor(1) as ex:
    for r in ex.map(one,names): print(r,flush=True)
