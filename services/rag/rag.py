from services.rag.embedding import get_embedding
from services.rag.search import search_similar_chunks
from services.rag.generate import generate_answer
from services.translation.translator import detect_language, translate_to_english, translate_from_english


def run_rag_pipeline(query: str) -> str:
    embedding = get_embedding(query)
    if not embedding:
        print("⚠️ No embedding generated, returning fallback.")
        return "Sorry, I didn't understand. Could you please repeat?"

    top_chunks = search_similar_chunks(embedding)
    answer = generate_answer(top_chunks, query)
    print(f"this is ansser {answer}")
    return answer

# def run_rag_pipeline(user_input: str) -> str:
#     user_lang = detect_language(user_input)
#     query_en = translate_to_english(user_input) if user_lang != "en" else user_input
#     print(f"🔤 Detected: {user_lang}, translated: {query_en}")

#     embedding = get_embedding(query_en)
#     if not embedding:
#         print("⚠️ No embedding generated, returning fallback.")
#         return "Sorry, I didn't understand. Could you please repeat?"

#     top_chunks = search_similar_chunks(embedding)
#     answer_en = generate_answer(top_chunks, query_en)

#     final_answer = (
#         translate_from_english(answer_en, user_lang) if user_lang != "en" else answer_en
#     )

#     return final_answer