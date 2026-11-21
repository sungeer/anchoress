from src import prompt, settings
from src.llm import chat
from src.memory import Memory
from src.tool import run_bash


def run(user_input, memory: Memory) -> str:
    user_message = {'role': 'user', 'content': user_input}
    memory.add(user_message)
    raw = chat(memory)
    return raw
