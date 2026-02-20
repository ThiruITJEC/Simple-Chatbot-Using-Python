import ollama
response=ollama.chat(
    model="gemma3:latest"
    messages=[
        {"role":"user","content":"Hey Bhai"}
        ]
)
print(response['message']['content'])
