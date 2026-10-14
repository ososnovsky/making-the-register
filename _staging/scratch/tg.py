import sys,re
sys.path.insert(0,'.')
from verify import fetch
st,fu,b=fetch("https://www.blablacommunity.com/events/blabla-and-make-friends-bratislava")
print(sorted(set(re.findall(r"https?://t\.me/[A-Za-z0-9_/+-]+",b)))[:5])
print(sorted(set(re.findall(r"https?://(?:www\.)?facebook\.com/[A-Za-z0-9_./-]+",b)))[:6])
