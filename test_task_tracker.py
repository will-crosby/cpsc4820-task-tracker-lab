"""Baseline tests for the Week 4 starter project.

These tests describe the CURRENT behavior of task_tracker.py. They should
pass before you delegate anything to an AI, and they should still pass
after (unless your chosen feature intentionally changes behavior — if so,
say why in your report).

Remember: per Assignment 4.1, you must also write at least two acceptance
tests of your own for the feature you delegate, and the AI may not modify
those tests.

Run with:  python -m pytest test_task_tracker.py
"""

import task_tracker as tt


def test_add_task_assigns_incrementing_ids():
    tasks = []
    t1 = tt.add_task(tasks, "first")
    t2 = tt.add_task(tasks, "second")
    assert t1["id"] == 1
    assert t2["id"] == 2
    assert len(tasks) == 2


def test_add_task_stores_title_and_tag():
    tasks = []
    task = tt.add_task(tasks, "study", tag="school")
    assert task["title"] == "study"
    assert task["tag"] == "school"
    assert task["done"] is False


def test_complete_task_marks_done():
    tasks = []
    tt.add_task(tasks, "a")
    result = tt.complete_task(tasks, 1)
    assert result is not None
    assert tasks[0]["done"] is True
    assert tasks[0]["completed"] is not None


def test_complete_missing_task_returns_none():
    assert tt.complete_task([], 99) is None


def test_delete_task_removes_it():
    tasks = []
    tt.add_task(tasks, "a")
    tt.add_task(tasks, "b")
    assert tt.delete_task(tasks, 1) is True
    assert len(tasks) == 1
    assert tasks[0]["title"] == "b"


def test_delete_missing_task_returns_false():
    assert tt.delete_task([], 42) is False


def test_filter_by_tag():
    tasks = []
    tt.add_task(tasks, "a", tag="school")
    tt.add_task(tasks, "b", tag="home")
    tt.add_task(tasks, "c", tag="school")
    filtered = tt.filter_tasks(tasks, tag="school")
    assert [t["title"] for t in filtered] == ["a", "c"]


def test_filter_open_only():
    tasks = []
    tt.add_task(tasks, "a")
    tt.add_task(tasks, "b")
    tt.complete_task(tasks, 1)
    filtered = tt.filter_tasks(tasks, include_done=False)
    assert [t["title"] for t in filtered] == ["b"]


def test_stats_counts():
    tasks = []
    tt.add_task(tasks, "a", tag="school")
    tt.add_task(tasks, "b")
    tt.complete_task(tasks, 1)
    s = tt.stats(tasks)
    assert s == {"total": 2, "done": 1, "open": 1, "by_tag": {"school": 1}}
