from flask import Flask, render_template, request, session
from groq import Groq

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
client = Groq(api_key='ENTER_YOUR_KEY')

@app.route("/", methods=["GET", "POST"])
def index():
    messages = session.get('messages', [])
    if request.method == "POST":
        user_input = request.form["input"]
        messages.append({"role": "user", "content": user_input})
        assistant_response = get_response(messages)
        messages.append({"role": "assistant", "content": assistant_response})
        session['messages'] = messages[-100:] 
    return render_template("index.html", messages=messages)

def get_response(messages_list):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages_list,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    return response
