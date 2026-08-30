import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from constants import system_prompt
from functions.move_tcp import move_tcp, schema_move_tcp


def main():
    t = time.time()
    if len(sys.argv) < 2:
        print("Please provide a prompt as an argument")
        raise OSError(1)
    available_functions = types.Tool(
        function_declarations=[schema_move_tcp],
    )

    prompt_tokens = 0
    response_tokens = 0

    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            print("User prompt:", sys.argv[1])
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]
    for i in range(0, 5):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
        except Exception as e:
            if "503" in str(e):
                print(f"Serwer przeciążony, retry za 3s...")
                time.sleep(3)
                continue
            raise
        print(f"API call: {time.time() - t:.2f}s")
        prompt_tokens += response.usage_metadata.prompt_token_count or 0
        response_tokens += response.usage_metadata.candidates_token_count or 0
        t = time.time()
        if response.function_calls is not None:
            function_responses = []
            for function in response.function_calls:
                if function.name == "move_tcp":
                    result = move_tcp(**function.args)
                    print(f"moveL: {time.time() - t:.2f}s")
                else:
                    result = {"error": f"Unknown function: {function.name}"}
                function_responses.append(
                    types.Part.from_function_response(
                        name=function.name,
                        response={"result": result},
                    )
                )
            messages.append(response.candidates[0].content)
            messages.append(types.Content(role="tool", parts=function_responses))
        if response.candidates:
            for canditate in response.candidates:
                messages.append(canditate.content)

        if not response.function_calls:
            if response.text:
                print(f"Final response:\n{response.text}")
                break


if __name__ == "__main__":
    main()
