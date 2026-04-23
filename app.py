from dotenv import load_dotenv
load_dotenv()

from chatbot.memory import ChatMemory
from chatbot.gemini_api import GeminiChat
from chatbot.router import route

def main():
    print("AI Chatbot (Gemini + Memory + Tools)")
    print("Type 'exit' to quit.\n")

    memory = ChatMemory()
    bot = GeminiChat()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        memory.add_user(user_input)

        decision = route(user_input)
        tool_text = decision["tool_text"]

        answer = bot.generate(
            user_input=user_input,
            memory_text=memory.as_text_block(),
            tool_text=tool_text
        )

        memory.add_assistant(answer)
        print(f"\nBot: {answer}\n")

if __name__ == "__main__":
    main()