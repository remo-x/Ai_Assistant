from call_functions import available_functions
from prompts import system_prompt
import os
from google import genai
from dotenv import load_dotenv
import argparse
from google.genai import types
from call_function import call_function
import sys


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Sorry boss I can't find the API key ;(")
    
    

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt",)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    

    got_final_result=False

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )
        if response.usage_metadata is None:
            raise RuntimeError("uhhhhhh idk, bot didn't wanna work ig :3")
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        candidates = response.candidates
        for candidate in candidates:
            messages.append(candidate.content)

        function_calls = response.function_calls

        print("Response:")
        if function_calls is not None:
            function_responses = []
            for function_call in function_calls:
                function_call_result = call_function(function_call, args.verbose)

                if not function_call_result.parts:
                    raise Exception("function_call_result.parts is empty!")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Something went wrong X3")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("oops, something went wrong")

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    print(f" - Calling function: {function_call.name}")
                function_responses.append(function_call_result.parts[0])
                
            messages.append(types.Content(role ="user",parts=function_responses,))


        else:
            print(response.text)
            got_final_result=True
            break

    if not got_final_result:
        print("Reached maximum iterations without a final response.")
        sys.exit(1)

    



        
if __name__ == "__main__":
    main()