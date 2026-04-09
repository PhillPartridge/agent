from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions


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
