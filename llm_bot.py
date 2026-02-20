# import ollama
# user_input=input("You: ")
# response=ollama.chat(
#     model="gemma3:latest",
#     messages=[
#         {"role":"user","content":user_input}
#         ]
# )
# print("Bot:",response['message']['content'])

## Looping of chatbot 
# import ollama
# while True:
#     user_input=input("You: ")

#     if user_input=="exit":
#         break
#     response=ollama.chat(
#         model="gemma3:latest",
#         messages=[
#             {"role":"user","content":user_input}
#             ]
#     )
#     print("Bot:",response['message']['content'])

## Add Memory
# import ollama
# messages=[]
# while True:
#     user_input=input("You: ")

#     if user_input=="exit":
#         break
#     messages.append({"role":"user","content":user_input}) #Stores each prompt
    
#     response=ollama.chat(
#         model="gemma3:latest",
#         messages=messages #giving input to all the chats
        
            
#     )
#     reply=response['message']['content']
#     print("Bot:",reply)
#     messages.append({"role":"user","content":reply}) #stores LLM Reply

#Adding the role of this Program    
import ollama
messages=[
    {"role":"system","content":"Act as Old Cheif Minister Selvi.Dr.J.Jayalalitha  conversastion in her tone"}
]
while True:
    user_input=input("You: ")

    if user_input=="exit":
        break
    messages.append({"role":"user","content":user_input}) #Stores each prompt
    
    response=ollama.chat(
        model="gemma3:latest",
        messages=messages #giving input to all the chats
        
            
    )
    reply=response['message']['content']
    print("Bot:",reply)
    messages.append({"role":"user","content":reply}) #stores LLM Reply
    