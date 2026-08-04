from dotenv import load_dotenv
from openai import OpenAI
from system_prompt import SYSTEM_PROMPT
import sys
load_dotenv()

try:
    client=OpenAI()
except Exception as e:
    print(f"Error creating OpenAI client: {e}")
    sys.exit(1)

def main():
    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        }
    ]

    print("-"*50)
    print("TaskBuddy: Hey there! what's on your mind?")
    print("               Dump your tasks here, and I'll organize them for you!")
    print("-"*50)

    while True:
        try:
            user_input=input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nTaskBuddy: Goodbye!")
                break
            messages.append({
                "role":"user",
                "content":user_input
            })
            response=client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            assistant_response=response.choices[0].message.content.strip()
            print("\nTaskBuddy:", assistant_response)
            messages.append({
                "role":"assistant",
                "content":assistant_response
            })
        except KeyboardInterrupt:
            print("\nTaskBuddy: Goodbye!")
            break
        except Exception as e:
            print(f"\n An error occured: {e}")
            break

if __name__ == "__main__":
    main()
       
