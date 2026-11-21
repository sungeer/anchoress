import os
import subprocess

from src import settings

# 参考 pi 的输出上限：只保留末尾 2000 行
MAX_LINES = 2000

_SYSTEM_ROOT = os.environ.get('SystemRoot', r'C:\Windows')


def run_bash(command: str, timeout: float | None = None) -> str:
    """在 Git Bash 中执行 command，工作目录是 settings.WORKSPACE。

    返回合并后的 stdout + stderr 和退出码；超过 2000 行时只保留末尾。
    timeout 单位为秒，不传则不限制。
    """
    if timeout is not None and (not isinstance(timeout, (int, float)) or timeout <= 0):
        return f'错误：timeout 必须大于 0 — timeout={timeout}'

    exe = settings.BASH_PATH

    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    try:
        proc = subprocess.Popen(
            [exe, '-c', command],
            cwd=settings.WORKSPACE,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=flags,
        )
    except OSError as e:
        return f'错误：无法启动 bash（{exe}）— {e}'

    timed_out = False
    try:
        raw, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_tree(proc.pid)
        raw, _ = proc.communicate()

    output = raw.decode('utf-8', errors='replace').replace('\r', '')
    body, truncated = _truncate_tail(output)
    body = body.rstrip('\n')

    if not body:
        body = '（无输出）'

    if truncated:
        body += f'\n\n[已截断：仅保留最后 {MAX_LINES} 行]'

    if timed_out:
        return f'{body}\n[错误：命令超时（{timeout} 秒），进程已终止]'

    return f'{body}\n[退出码 {proc.returncode}]'


def _kill_tree(pid: int) -> None:
    """杀掉 bash 及其子进程，防止子进程占着输出管道"""
    subprocess.run(
        [os.path.join(_SYSTEM_ROOT, 'System32', 'taskkill.exe'), '/F', '/T', '/PID', str(pid)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _truncate_tail(text: str, max_lines: int = MAX_LINES) -> tuple[str, bool]:
    """从末尾保留 max_lines 行，返回 (内容, 是否截断)"""
    lines = text.split('\n')
    if text.endswith('\n'):
        lines.pop()

    if len(lines) <= max_lines:
        return text, False

    return '\n'.join(lines[-max_lines:]), True
