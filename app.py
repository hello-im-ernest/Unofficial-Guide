import gradio as gr
from retriever import embed_and_store, retrieve
from generator import generate_response

print("Initializing database...")
embed_and_store()
print("Ready!")

def ask(question):
    if not question.strip():
        return "Please enter a question.", ""
    chunks = retrieve(question)
    result = generate_response(question, chunks)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="SPC Unofficial Guide") as demo:
    gr.Markdown("# 🎓 St. Philip's College Unofficial Guide")
    gr.Markdown("Real student knowledge about surviving and thriving at SPC.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. What is the Alamo Promise?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=3)
    
    btn.click(ask, inputs=inp, outputs=[answer, sources])
    inp.submit(ask, inputs=inp, outputs=[answer, sources])

demo.launch()