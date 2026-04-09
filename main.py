import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.generate_response import generate_response
from functions.call_functions import call_function
from config import LOOP_LIMIT


def main():
    print("Hello from agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("RuntimeError found: unable to retrieve api_key")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(
        description="This is an agent that should help you"
    )
    parser.add_argument("user_prompt", type=str, help="Please input your user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(LOOP_LIMIT):
        result_of_functions = []
        response = generate_response(client, messages)
        for c in response.candidates or []:
            if c.content is not None:
                messages.append(c.content)

        promptTokens, responseTokens = get_prompt_info(response)

        if args.verbose:
            print(
                f"User prompt: {args.user_prompt}\n"
                f"Prompt tokens: {promptTokens}\n"
                f"Response tokens: {responseTokens}\n"
            )

        if response.function_calls:
            for f in response.function_calls:
                function_call_result = call_function(f)
                if not function_call_result.parts:
                    raise RuntimeError(
                        f"Error: Function {f} did not contain parts list"
                    )
                if not function_call_result.parts[0].function_response:
                    raise RuntimeError("Error: first function response equals None")
                if not function_call_result.parts[0].function_response.response:
                    raise RuntimeError(
                        "Error: first function response contained zero response"
                    )

                result_of_functions.append(function_call_result.parts[0])

                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

            messages.append(types.Content(role="user", parts=result_of_functions))
        elif response.text:
            print(f"Response:\n{response.text}")
            break
    else:
        print(f"LOOP_LIMIT [{LOOP_LIMIT}] has been reached without final response")
        sys.exit(1)


def get_prompt_info(promptInfo) -> tuple[int, int]:
    if promptInfo is None:
        raise RuntimeError("RuntimeError occurred: repsonse was empty")
    return (
        promptInfo.usage_metadata.prompt_token_count,
        promptInfo.usage_metadata.candidates_token_count,
    )


if __name__ == "__main__":
    main()
