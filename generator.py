import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def generate_response(query, retrieved_chunks):
    if not retrieved_chunks:
        return {
            "answer": "I couldn't find anything relevant in the loaded documents. Try rephrasing your question.",
            "sources": []
        }

    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        context += f"[Source {i+1} - {chunk['source']}]\n{chunk['text']}\n\n"

    response = _client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful student guide for St. Philip's College. "
                    "Answer using only the information in the provided documents. "
                    "Do not draw on outside knowledge. "
                    "If the documents don't contain enough information to answer, say so explicitly. "
                    "Always state which source document your answer comes from."
                )
            },
            {
                "role": "user",
                "content": f"Here are the relevant documents:\n\n{context}\nQuestion: {query}"
            }
        ]
    )

    sources = list(set(chunk["source"] for chunk in retrieved_chunks))
    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }