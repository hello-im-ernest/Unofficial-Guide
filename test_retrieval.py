from retriever import retrieve

results = retrieve("What do students say about the registration process?")
for r in results:
    print(f"[{r['source']}] (dist: {r['distance']:.3f})")
    print(r['text'][:150])
    print()