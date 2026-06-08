from retriever import retrieve
from generator import generate_response

query = "What is the Alamo Promise and who is eligible?"
chunks = retrieve(query)

print("=== RETRIEVED CHUNKS ===")
for c in chunks:
    print(f"[{c['source']}] (dist: {c['distance']:.3f})")
    print(c['text'][:200])
    print()

result = generate_response(query, chunks)
print("=== ANSWER ===")
print(result["answer"])
print("\nSources:", result["sources"])