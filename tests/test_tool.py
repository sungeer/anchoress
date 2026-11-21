import pytest

from src import settings
from src.tool import run_bash


@pytest.fixture(autouse=True)
def _workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, 'WORKSPACE', tmp_path)


def test_echo_and_exit_code():
    result = run_bash('echo hi')
    assert 'hi' in result
    assert '[退出码 0]' in result


def test_cwd_is_workspace(tmp_path):
    (tmp_path / 'a.txt').write_text('x', encoding='utf-8')
    assert 'a.txt' in run_bash('ls')


def test_nonzero_exit_code():
    assert '[退出码 3]' in run_bash('exit 3')


def test_stderr_captured():
    assert 'boom' in run_bash('echo boom >&2')


def test_cr_stripped():
    result = run_bash(r"printf 'a\r\nb\n'")
    assert '\r' not in result


def test_timeout():
    assert '超时' in run_bash('sleep 5', timeout=1)


def test_output_truncated():
    result = run_bash('seq 1 3000')
    assert '已截断' in result
    body = result.split('\n\n[已截断')[0]
    lines = body.split('\n')
    assert len(lines) == 2000
    assert lines[0] == '1001'
    assert lines[-1] == '3000'


def test_invalid_timeout():
    assert '错误' in run_bash('echo hi', timeout=0)
