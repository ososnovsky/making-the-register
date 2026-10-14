import sys,glob,re
ids=set(sys.argv[1:])
for f in glob.glob('cand/*.txt'):
    L=open(f,encoding='utf-8').read().split("\n")
    K=[l for l in L if l.split(" |")[0] not in ids]
    if len(K)!=len(L): open(f,'w',encoding='utf-8').write("\n".join(K)); print(f,len(L)-len(K))
