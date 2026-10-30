import sys
sys.stdout.reconfigure(encoding='utf-8')
from backend.app.services.rag.retriever import HybridRetriever

r = HybridRetriever()
queries = [
    'પશુપાલન ખાતાની સહાયકારી યોજનાઓ કઈ કઈ છે?',
    'દાડમની ખેતીમાં કઈ જાતો અનુકૂળ આવે છે?',
    'ICAR soil health testing methods in India',
    'કપાસના પાકની વૈજ્ઞાનિક ખેતી પદ્ધતિ જણાવો'
]

for q in queries:
    chunks = r.retrieve(q, top_k=3)
    print(f"\nQuery: {q}")
    print(f"Retrieved {len(chunks)} chunks:")
    for c in chunks:
        doc = c.get('document_name')
        sub = c.get('subfolder')
        sim = c.get('similarity_score')
        comb = c.get('combined_score')
        txt = c.get('text', '')[:100].replace('\n', ' ')
        print(f"  - [{sub}/{doc}] Sim: {sim} | Comb: {comb}")
        print(f"    Text: {txt}...")

