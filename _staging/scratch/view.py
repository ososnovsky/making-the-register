import sys,re
for l in open(sys.argv[1],encoding='utf-8'):
    p=[x.strip() for x in l.rstrip().split(" | ")]
    if len(p)<8: print(l[:200]); continue
    name,st,fu,title,y,addr,ag,nl=p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7]
    if st not in("200",): print(f"X{st} {name[:40]}"); continue
    a=ag.replace("AG: ","").split()
    print(f"{name[:42]} | {fu[:40]+' ' if fu else ''}{title[:38]} | {y} | {addr[6:50]} | {a[0][:70] if a else ''} | {'NL' if nl.strip()!='NL:' else ''}")
