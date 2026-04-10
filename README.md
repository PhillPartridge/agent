# AI Agent

A command-line AI agent powered by the Google Gemini API. Accepts a user prompt, invokes tools via function calling, and iterates until a final text response is produced or the loop limit is reached.

## Requirements

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`
- A valid Gemini API key

## Installation

```bash
uv sync

## Usage

```bash
python main.py "Your prompt here"
```

### Flags

| Flag        | Description             |
|-------------|-------------------------|
| `--verbose` | Print token usage and function call responses |

### Examples

```bash
python main.py "What files are in the current directory?"
python main.py "Summarise the contents of notes.txt" --verbose
```

## Project Structure

```
.
├── main.py                  # Entry point and agentic loop
├── config.py                # Constants (e.g. LOOP_LIMIT)
├── prompts.py               # System prompt definition
├── functions/
│   └── call_functions.py    # Function dispatch and tool declarations
└── .env                     # API key (not committed)
```

## How It Works

1. The user prompt is added to the message history.
2. A request is sent to Gemini with the available tools and system prompt.
3. If the model returns function calls, they are executed and the results are appended to the message history.
4. Steps 2–3 repeat until the model returns a plain text response or `LOOP_LIMIT` is hit.
