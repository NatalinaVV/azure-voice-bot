from services.rag.embedding import get_embedding
from services.rag.search import search_similar_chunks
from services.rag.generate import generate_answer

def run_rag_pipeline(query: str) -> str:
    embedding = get_embedding(query)
    if not embedding:
        print("⚠️ No embedding generated, returning fallback.")
        return "Sorry, I didn't understand. Could you please repeat?"

    top_chunks = search_similar_chunks(embedding)
    answer = generate_answer(top_chunks, query)
    print(f"this is ansser {answer}")
    return answer