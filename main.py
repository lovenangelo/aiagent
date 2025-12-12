import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("Gemini API Key is not set")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_write_file, schema_run_python_file, schema_get_file_content],
)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    responses = []

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT),
    )

    if response.usage_metadata == None:
        raise RuntimeError("API Request failed")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for candidate in response.candidates():
        messages.append(candidate.content)

    if response.function_calls != None:
        for fc in response.function_calls:
            result = call_function(fc, args.verbose)
            if len(result.parts) == 0:
                raise Exception("Error: something went wrong")
            else:
                new_message = types.Content(role: 'user', result.parts)
                messages.append(new_message)
                responses.append(result.parts[0])
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")

    else:
        print(response.text)


if __name__ == "__main__":
    main()
