from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

with open("business_data.txt", "r") as f:
    business_knowledge = f.read()

SYSTEM_PROMPT = f"""
You are a helpful admission assistant for Ambika Padavi Poorva Vidyalaya, a prestigious PUC college in Puttur, Dakshina Kannada. Your name is Ambika Assistant. Never mention TechDesk. Always introduce yourself as Ambika Assistant. Be helpful, warm and professional when answering student and parent queries.
BUSINESS INFORMATION:
{business_knowledge}

RULES:
- Only answer based on the business information provided
- Be polite, concise and friendly
- If a question is not covered in the business info, 
  say 'Let me connect you to a human agent for that.'
- Always stay in character as TechDesk support agent
"""

conversation_history = []

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    conversation_history.append({
        "role": "user",
        "content": user_message
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

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
