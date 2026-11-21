from src import settings
from src.http import httpx
from src.memory import Memory


def chat(memory: Memory) -> str:
    url = 'https://api.deepseek.com/chat/completions'

    headers = {
        'Authorization': f'Bearer {settings.LLM_KEY}',
        'Content-Type': 'application/json'
    }

    messages: list = memory.get_messages()

    payload = {
        'model': settings.LLM_MODEL,
        'messages': messages,
        'stream': False,
        'thinking': {'type': 'disabled'}
    }

    client = httpx.get_client()

    response = client.post(url, headers=headers, json=payload)

    response.raise_for_status()

    data = response.json()
    # print(f'llm response data:\n{data}')

    choices = data.get('choices')
    choice, *_ = choices

    message = choice.get('message')

    content = message.get('content')

    return content
