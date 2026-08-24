# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

CLI tool that reads the staged `git diff`, sends it to an LLM (via OpenRouter), and returns a conventional-commit message. Python 3.12+, managed with `uv`.

## Commands

```bash
uv sync                                        # install deps + the package (editable)
uv run commit-msg-generator                    # run the tool (console entry point)
uv run python -m commit_msg_generator.main     # equivalent module invocation
uv run pytest                                  # run all tests
uv run pytest tests/unit/test_main.py::test_name  # run a single test
uv run mypy src/commit_msg_generator           # type-check the package
```

`OPENROUTER_API_KEY` must be set in `.env` (loaded via `dotenv`). `main.py` calls `load_dotenv()` and fails fast at startup if the key is missing; `llm.py` re-checks it before making a request.

## Architecture

The code is a proper package at `src/commit_msg_generator/` (src-layout, built by hatchling, exposed as the `commit-msg-generator` console script — see `pyproject.toml`). Modules import each other with **relative imports** (`from . import git`, `from .models import GitDiffMsg`), so run it as a package (`-m` or the console script), not by executing a file directly.

The pipeline is: `git.diff()` (staged diff) → `parser.extract_git_diff()` (unified diff → hunks) → `llm.LLM.run_llm()` (diff → validated commit message). `main.py` is the entrypoint that wires these together.

- **git.py** — thin subprocess wrapper over the git CLI. `diff()` runs `git diff --staged`; `commit()` records the message. Non-zero exits raise `GitError`.
- **parser.py** — regex line-walker that splits a unified diff into per-hunk `ChunkMsg`s, tracking the current file and each `@@` hunk's new-file start line.
- **models.py** — dataclasses `ChunkMsg` (file, start line, text) and `GitDiffMsg` (list of chunks + raw text). (Named `models.py`, not `types.py`, to avoid shadowing the stdlib `types` module.)
- **llm.py** — the core. Iterates a `default_model` + `fallback_models` chain. Errors are partitioned into three tiers: `FATAL` (auth/bad-request → raise `LLMError` immediately), `RETRY` (rate-limit/5xx/timeout/bad-output → back off `2 ** attempt` and retry the same model), and `REROUTE` (provider-overloaded/not-found/validation → skip to the next model). The model is asked for a JSON object `{"model", "commit_message"}`; `_extract_json` tolerates fenced/prose-wrapped JSON, and the message is validated with `PREFIX_RE` (conventional-commit type + optional scope/`!`) and a ≤100-char description, raising `CommitMsgError` (a `RETRY` type) on failure.

## Current state

This is a work in progress. `main.py` currently stops after parsing and does not yet call `llm`. `cli.py` and `prompt.py` exist but are empty — diff-size measurement/truncation is intended to live in `prompt.py` (a prompt creation/formatting module), not `llm.py`. Test files (`tests/unit/test_main.py`) are empty stubs. `llm.py`'s former inline backlog (three-tier error handling, empty-diff guard, JSON-shape validation, regex prefix validation, logging, generation params, fail-fast key check) is now implemented.
