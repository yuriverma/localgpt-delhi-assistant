from llama_cpp import Llama

llm = Llama(
    model_path="models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=1024,      # Use 512 if 1024 crashes
    n_threads=4,     # You can adjust this based on CPU
    use_mlock=True   # Locks memory to prevent swap
)

def generate_response(prompt: str):
    output = llm(prompt, max_tokens=200, stop=["User:", "\n\n"])
    return output["choices"][0]["text"].strip()

