import os

from dotenv import load_dotenv

load_dotenv()


def get_assistant_name():
    return os.getenv("ASSISTANT_NAME", "Assistant")

def get_user_input():
    return input("Usuario: ")

def call_ai_model(prompt):
    # Placeholder for AI model call
    # In a real implementation, this would call the OpenAI API or another AI service
    return f"IA Responde: {prompt}"

def main():
    assistant_name = get_assistant_name()
    print(f"{assistant_name}: Hola! ¿Cómo puedo ayudarte hoy?")

    while True:
        user_input = get_user_input()
        if user_input.lower() in ["exit", "quit","salir", "chau"]:
            
            print(f"{assistant_name}: ¡Hasta luego!")
            break

        response = call_ai_model(user_input)
        print(f"{assistant_name}: {response}")


if __name__ == "__main__":
    main()