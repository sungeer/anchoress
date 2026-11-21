import logging

from src.memory import Memory
from src.prompt import system_prompt
from src.http import httpx
from src import agent

logger = logging.getLogger(__name__)


def main() -> None:
    httpx.init()

    print('* An agentic tool that lives in your terminal.')
    print('* Press /exit to quit, /clear to clear memory')

    system_message = {'role': 'system', 'content': system_prompt}
    memory = Memory()
    memory.add(system_message)

    while True:
        try:
            user_input = input('\n> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\n* Bye！')
            break

        if not user_input:
            continue

        if user_input.lower() in ('/exit', '/q', '/quit'):
            print('\n* Bye！')
            break

        if user_input.lower() == '/clear':
            memory.clear()
            memory.add(system_message)
            print('* 记忆已清空，开始新对话')
            continue

        try:
            result = agent.run(user_input, memory)
        except Exception as exc:
            print(f'● 本次请求失败:\n{exc}')
            continue

        print(f'● {result}')
