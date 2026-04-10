import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_functions import call_function, available_functions
from prompts import system_prompt
from config import LOOP_LIMIT


def main():
    print("Hello from agent!")
    args = parse_args()
    client = build_client()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(LOOP_LIMIT):
        result_of_functions = []
        response = generate_response(client, messages)
        for c in response.candidates or []:
            if c.content is not None:
                messages.append(c.content)

        prompt_tokens, response_tokens = get_prompt_info(response)

        if args.verbose:
            print(
                f"User prompt: {args.user_prompt}\n"
                f"Prompt tokens: {prompt_tokens}\n"
                f"Response tokens: {response_tokens}\n"
            )

        if response.function_calls:
            result_of_functions = handle_function_calls(response, args.verbose)
            messages.append(types.Content(role="user", parts=result_of_functions))
        elif response.text:
            print(f"Response:\n{response.text}")
            break
    else:
        print(f"LOOP_LIMIT [{LOOP_LIMIT}] has been reached without final response")
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This is an agent that should help you"
    )
    parser.add_argument("user_prompt", type=str, help="Please input your user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def build_client() -> genai.Client:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("RuntimeError found: unable to retrieve api_key")
    return genai.Client(api_key=api_key)


def generate_response(
    client: genai.Client, messages: list
) -> types.GenerateContentResponse:
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )


def get_prompt_info(promptInfo) -> tuple[int, int]:
    if promptInfo is None:
        raise RuntimeError("RuntimeError occurred: response was empty")
    return (
        promptInfo.usage_metadata.prompt_token_count,
        promptInfo.usage_metadata.candidates_token_count,
    )


def handle_function_calls(response, verbose: bool) -> list:
    result = []
    for f in response.function_calls:
        function_call_result = call_function(f)
        if not function_call_result.parts:
            raise RuntimeError(f"Error: Function {f} did not contain parts list")
        if not function_call_result.parts[0].function_response:
            raise RuntimeError("Error: first function response equals None")
        if not function_call_result.parts[0].function_response.response:
            raise RuntimeError("Error: first function response contained zero response")

        result.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    return result


if __name__ == "__main__":
    main()
