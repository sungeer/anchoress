import textwrap

from src import prompt, settings, utils
from src.llm import chat
from src.memory import Memory
from src.tool import run_bash


def run(user_input, memory: Memory, max_steps: int = 100) -> str:
    for step in range(1, max_steps + 1):
        user_message = {'role': 'user', 'content': user_input}
        memory.add(user_message)

        content = chat(memory)

        assistant_message = {'role': 'assistant', 'content': content}
        memory.add(assistant_message)

        command = utils.split_bash(content)

        if not command:
            return content

        output = run_bash(command)

        user_input = textwrap.dedent(f'''
            [Tool Result] Bash 命令执行完毕，输出如下：
            {output}
            请根据以上结果继续回答用户的问题。
        ''').strip()

    return f'已达工具调用上限（{max_steps} 轮），本轮中断。可以回复「继续」接着做。'
