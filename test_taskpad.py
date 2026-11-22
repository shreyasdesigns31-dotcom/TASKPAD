import pytest

from taskpad.cli import main
from taskpad.storage import TaskStore


@pytest.fixture
def path(tmp_path):
    return tmp_path / "tasks.json"


def test_add_assigns_incrementing_ids(path):
    store = TaskStore(path)
    assert store.add("first").id == 1
    assert store.add("second").id == 2


def test_add_rejects_empty_title(path):
    with pytest.raises(ValueError):
        TaskStore(path).add("   ")


def test_tasks_persist_between_instances(path):
    TaskStore(path).add("persist me")
    assert [t.title for t in TaskStore(path).tasks] == ["persist me"]


def test_ids_stay_unique_after_removal(path):
    store = TaskStore(path)
    store.add("a")
    store.add("b")
    store.remove(1)
    assert store.add("c").id == 3


def test_complete_and_clear_done(path):
    store = TaskStore(path)
    store.add("a")
    store.add("b")
    store.complete(1)
    assert store.clear_done() == 1
    assert [t.title for t in store.tasks] == ["b"]


def test_missing_task_raises(path):
    with pytest.raises(KeyError):
        TaskStore(path).complete(99)


def test_corrupt_file_raises_value_error(path):
    path.write_text("{not json")
    with pytest.raises(ValueError):
        TaskStore(path)


def test_cli_flow(path, capsys):
    f = ["--file", str(path)]
    assert main(f + ["add", "write", "tests"]) == 0
    assert main(f + ["list"]) == 0
    assert "write tests" in capsys.readouterr().out
    assert main(f + ["done", "1"]) == 0
    capsys.readouterr()
    main(f + ["list"])
    assert "Nothing to do" in capsys.readouterr().out
    main(f + ["list", "--all"])
    assert "[x]" in capsys.readouterr().out


def test_cli_reports_errors(path, capsys):
    assert main(["--file", str(path), "done", "42"]) == 1
    assert "error:" in capsys.readouterr().err
