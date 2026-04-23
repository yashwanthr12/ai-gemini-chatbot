from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for
from chatbot.memory import ChatMemory
from chatbot.gemini_api import GeminiChat
from chatbot.router import route
from utils.logger import setup_logger

logger = setup_logger("web_app")

app = Flask(__name__)

memory = ChatMemory()
bot = GeminiChat()

@app.route("/", methods=["GET", "POST"])
def index():
    global memory
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        if text:
            logger.info("User input: %s", text)
            memory.add_user(text)

            decision = route(text)
            tool_text = decision["tool_text"]

            answer = bot.generate(
                user_input=text,
                memory_text=memory.as_text_block(),
                tool_text=tool_text
            )
            memory.add_assistant(answer)

        return redirect(url_for("index"))

    return render_template("index.html", messages=memory.messages)

if __name__ == "__main__":
    app.run(debug=True, port=5000)