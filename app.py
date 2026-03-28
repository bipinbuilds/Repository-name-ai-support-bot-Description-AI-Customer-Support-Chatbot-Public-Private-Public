from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

with open("business_data.txt", "r", encoding="utf-8") as f:
    business_knowledge = f.read()

SYSTEM_PROMPT = f"""
You are Ambika, a friendly admission counselor for
Ambika Padavi Poorva Vidyalaya in Puttur, Dakshina Kannada.

COLLEGE INFORMATION:
{business_knowledge}

STRICT RULES FOR RESPONSES:
- Keep answers SHORT and CRISP
- Use bullet points whenever listing anything
- Maximum 3-4 lines per response
- Never write long paragraphs
- Be warm and friendly like a real counselor
- If question not covered say 'Please call us at +91 94488 35488'
- Never make up information
- Always end with a helpful follow up question
"""

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        if not data or "message" not in data:
            return jsonify({"reply": "Please send a message!"}), 400

        user_message = data["message"]
        conversation = data.get("history", [])

        conversation.append({
            "role": "user",
            "content": user_message
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + conversation,
            max_tokens=500,
            temperature=0.7
        )

        bot_reply = response.choices[0].message.content

        conversation.append({
            "role": "assistant",
            "content": bot_reply
        })

        return jsonify({
            "reply": bot_reply,
            "history": conversation
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"reply": "I apologize, please ask your question again!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)