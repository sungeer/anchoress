# hostess

A minimal AI coding agent that runs in your terminal. One tool, one loop, no framework.

## Why this exists

Corporate intranets forbid installing third-party coding tools, and only a limited set of
packages is available. This project started from a ReAct loop script and grew into a working
substitute.

It is meant to read project code, write documentation, write demos, find bugs, and produce
revised code modules.

Design constraints follow from that:

- **One tool only.** `bash`. Nothing else.
- **No high-risk tools.** The agent never modifies existing files; it answers with a unified
  diff you apply yourself.
- **High user competence assumed.** This is not a one-click tool. You review what it does.

## How it works

`run.py` starts a REPL. Each turn sends the whole conversation to a chat completions endpoint.
If the reply contains a ```` ```bash ```` block, that block is run in Git Bash, and its output is
sent back as the next message so the model can continue. When a reply has no ```` ```bash ```` block,
that reply is the final answer. One turn is capped at 100 LLM calls.

This is prompt convention, not function calling: the model is told to use ```` ```text ```` fences
when it wants to show shell examples rather than run them.

## Requirements

- Python 3.10+
- Git Bash on Windows (`bash.exe`)

```bash
python -m pip install python-dotenv httpx2
```

For tests: `python -m pip install pytest`

## Quick Start

Create a `.env` in the project root (see `.env.example`):

```bash
API_BASE_URL=https://api.deepseek.com
API_KEY=sk-no-key
MODEL=deepseek-flash
BASH_PATH=C:\Apps\Git\bin\bash.exe
```

`BASH_PATH` is required — there is no fallback. Start the agent from the directory you want it
to work in:

```bash
python run.py
```

Or `bin/hostess.bat` if the paths inside match your machine.

## Endpoint

`src/llm.py` currently posts to `https://api.deepseek.com/chat/completions` and sends
`thinking: {type: disabled}`, a DeepSeek-specific field. Point it at another
OpenAI-compatible endpoint and you must change the URL in code and probably drop that field.
`API_BASE_URL` is loaded into `settings.LLM_URL` but not yet used.

## Commands

| Command | Description |
|---------|-------------|
| `/clear` | Clear conversation history |
| `/exit` `/q` `/quit` | Quit |

## Tools

| Tool | Function | Parameters |
|------|----------|------------|
| `bash` | Run a bash command in the startup directory; returns merged stdout + stderr line count capped at the last 2000 lines, then the exit code | `command`, `timeout` (seconds, no timeout by default) |

Listing, searching and reading all go through `bash`: `ls`, `find`, `rg`, `cat`, `sed -n`.
Writing a new file goes through `bash` too, via heredoc; existing files are not overwritten.
