"""python addlink.py file.tsv  lines: id<TAB>url<TAB>code<TAB>note  -> appends link to the entry's links field in cand/*.txt"""
import sys,glob,re
adds={}
for l in open(sys.argv[1],encoding='utf-8'):
    p=l.rstrip("\n").split("\t")
    if len(p)<3 or l.startswith("#"): continue
    adds.setdefault(p[0],[]).append(f"{p[1]}@{p[2]}"+(f"~{p[3]}" if len(p)>3 and p[3] else ""))
done=set()
for f in glob.glob('cand/*.txt'):
    L=open(f,encoding='utf-8').read().split("\n"); ch=False
    for i,l in enumerate(L):
        eid=l.split(" |")[0]
        if eid in adds:
            fl=re.split(r" \|(?= |$)",l)
            fl[2]=fl[2].strip()+" ; "+" ; ".join(adds[eid])
            L[i]=" |".join([fl[0]]+[" "+x.strip() if x.strip() else " " for x in fl[1:]]).replace("|  |","| |")
            # normalise spacing: rebuild with ' | '
            parts=[x.strip() for x in fl]
            L[i]=" | ".join(parts[:-1])+" |" if parts[-1]=="" else " | ".join(parts)
            L[i]=L[i].replace(" |  | "," | | ")
            done.add(eid); ch=True
    if ch: open(f,'w',encoding='utf-8').write("\n".join(L))
print("updated",len(done),"missing",set(adds)-done)
