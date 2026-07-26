# Week 4 Starter Repo — Task Tracker

CPSC 4820/6820 · AI-Receptive Software Development · Summer 2026

A small, working command-line task manager. It stores tasks in a local
`tasks.json` file. This repo is the optional starting point for
**Assignment 4.1: Delegate & Review Lab** — you may also use your own
project of similar size instead.

## Setup

Requires Python 3.9+ and pytest (`pip install pytest`).

```
python task_tracker.py add "Read week 4 module" --tag school
python task_tracker.py list
python task_tracker.py done 1
python task_tracker.py stats
python -m pytest          # all baseline tests should pass
```

## How to use this repo for Assignment 4.1

1. Unzip, then verify the baseline tests pass on `main`.
2. Create a feature branch — **the AI never works on main**.
3. Pick ONE feature to delegate (ideas below), write your acceptance
   criteria and at least two of your own tests first, then follow the
   assignment instructions.

## Feature ideas (pick one, moderate scope on purpose)

- **Input validation & error handling**: reject empty/whitespace titles,
  handle a corrupted `tasks.json` gracefully, friendly errors for bad ids.
- **Due dates**: `add --due 2026-08-02`, show overdue tasks in `list`,
  and a `list --overdue` flag.
- **Priorities**: `add --priority high|med|low`, sort `list` by priority.
- **Search**: a `search <keyword>` command matching against titles.
- **Edit command**: `edit <id> --title/--tag` with sensible rules for
  completed tasks.

Each of these touches multiple functions plus tests — big enough to be
worth delegating, small enough to review every line. That is the point.

## Rules reminder

- Your own acceptance tests may not be modified by the AI.
- The baseline tests in `test_task_tracker.py` should still pass unless
  your feature intentionally changes behavior (explain if so).
- Commit in small, intent-revealing units and attribute AI assistance
  per the assignment.
