import re

_bash_block = re.compile(r'^```bash\n(.*?)^```', re.DOTALL | re.MULTILINE)


def split_bash(content: str) -> str | None:
    m = _bash_block.search(content)
    return m.group(1) if m else None
