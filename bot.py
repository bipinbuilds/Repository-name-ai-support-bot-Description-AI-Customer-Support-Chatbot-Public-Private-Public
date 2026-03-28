from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
SYSTEM_PROMPT = """
You are a helpful customer support assistant.
Be polite, concise and helpful.
If you don't know the answer, say 
'Let me connect you to a human agent.'
"""

print("🤖 AI Support Bot is running! Type 'quit' to stop.")
print("-" * 50)

conversation_history = []

while True:
    user_input = input("Customer: ")
    
    if user_input.lower() == "quit":
        print("Bot: Goodbye! Have a great day!")
        break
    
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + conversation_history
    )
    
    bot_reply = response.choices[0].message.content
    
    conversation_history.append({
        "role": "assistant",
        "content": bot_reply
    })
    
    print(f"Bot: {bot_reply}")
    print("-" * 50)
