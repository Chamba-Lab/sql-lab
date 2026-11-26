# Agent instructions

This repository is a study path built with [StudyForge](https://github.com/Chamba-Lab/studyforge) (version in `studyforge.toml`). It is the single source of instructions for any AI agent; `CLAUDE.md` only imports it.

## Start here (fresh session)
1. Read this file, `SYLLABUS.md` (plan, status, notes for the next labs) and `docs/lessons.md`.
2. Run `git status` and `git log --oneline -15` to see where the work stands.
3. If the StudyForge skill is installed, use it: `build` for the next ⬜ `pending` item in syllabus order (do not ask which), `feedback` when a learner reports on a lab, `review` to audit or upgrade.
4. Without the skill, follow the rules below and the method at https://github.com/Chamba-Lab/studyforge/tree/master/skills/studyforge.

## Context
- **Learner:** a group of the [Chamba Lab](https://chambalab.org) community looking for their first job, Spanish-speaking. They know basic Python (functions, lists, dicts, some classes, reading files) and spreadsheets (Excel filters, some pivot tables). Most never used a database; a few wrote a simple `SELECT … WHERE` once. They use the terminal little (`python file.py`, `pip install`), know basic Git (clone, add, commit, push) and have never used pytest. Plan for the least experienced.
- **Goal:** query, design and look after relational databases with SQL, at the level of a first job and its technical interviews.
- **Stack:** Python 3.12+ (labs are verified on 3.12 and 3.15, the CI matrix) with the standard-library `sqlite3` module (SQLite bundled with Python, 3.45 or newer in the builds measured; see `docs/decisions.md`), pytest 9.2.0. Versions live in `requirements.txt` and are upgraded together.
- **Learner environment:** Windows first (PowerShell, then Bash), VS Code; no containers, no separate SQLite install. Everything must also work on macOS and Linux.

## Working agreement
- Chat in the learner's language; lab content in Spanish (`language.content = "es"`, neutral Spanish, no local slang); code, identifiers, folders and commits in English. SQL keywords in upper case in every lab.
- Terms of art stay in English, glossed in Spanish the first time (JOIN, query plan, primary key / clave primaria, window function; StudyForge `references/didactics.md`). Section titles use the Spanish column of StudyForge's reference table (`references/writing.md`); *Command dissection* stays in English.
- Every new concept goes problem → idea → minimal example → name, before a task needs it, and the idea comes before the SQL that writes it.
- Decide and recommend; do not hand decisions back. Scope, depth and anything outward-facing (remote repositories, publishing, CI) are the maintainer's call: compare briefly, recommend, wait.
- One lab at a time. Labs stay 🟨 `built` until a learner solved them and their feedback was applied; only then ✅ `done`.
- Report outcomes faithfully: what passed, what failed, what was not run.

## Talking with the learner
- Answer first, in a few lines. A longer explanation goes into the lab (Concepts or `CONCEPT.md`); point to it instead of pasting it.
- One question at a time. At most three when unavoidable, numbered, each with options and a recommended answer.
- Predictions are the learner's: never give the answer to a 🔮 prediction, even after a guess; ask them to run it, then explain what they got.
- A hint before the solution: a question, then a more concrete hint, full code only when asked. Do not edit the learner's code unless asked.
- Check understanding with one question, not a quiz.
- Say only what changes for the learner; no recap of everything you read or ran.
- End every reply with the next step: "Tu siguiente paso: …".
- `TUTOR.md` carries these rules for learners who study in a chat; when one of them changes, change it there too.

## Repository rules
- Layout, names and IDs follow StudyForge (`labs/NN-block/NN-slug`, `project-<domain>` last in its block; IDs freeze once `built`).
- `master` is the clean template. Learners keep solutions in `solutions/<name>` or a fork; never commit solved starters here.
- Conventional Commits: `feat(lab-1.2): …`, `feat(project-1): …`, `fix(lab-…)`, `docs(syllabus): …`. Push at milestones or on request.
- Never commit secrets or `.env`. No byte-order marks. LF line endings (`.gitattributes`).
- No real usernames, home paths or e-mail addresses in repository files, lessons and verified outputs included: write `C:/Users/<user>/…` or `~/…`. Before committing, `git grep` the tracked files for your own username and home path.
- Every claim in a lab was run on the pinned versions. `python tools/verify.py --lab <ID>` must pass before a lab is `built`.

## Stack specifics
- **One virtual environment** at the repository root (`.venv`, from `requirements.txt`). Each lab variant has its own `pyproject.toml` with only `[tool.pytest]` (native TOML configuration, pytest 9+): `testpaths = ["tests"]`, `pythonpath = ["."]`; no packaging.
- **Blocks 1–4: the learner writes `.sql` files.** Each task is one file in `starter/` holding only a `-- TODO` comment; `solution/` holds the same files solved. The tests create a fresh in-memory database from the lab's seed script for every test, run the learner's file and compare rows. A `-- TODO` file returns no rows, so the target test fails on the comparison, not on a syntax error. The harness is fixed in lab 1.2; copy it from there.
- **Block 5: the learner writes Python** that uses `sqlite3`. Code labs follow the stack note: the function under study raises `NotImplementedError("TODO")`.
- **Projects are atomic:** `project-*/reference` declares its own dependencies in its `pyproject.toml` and does not rely on lab code.
- **Do not depend on the SQLite version.** Python builds bundle different SQLite versions (3.45.3 to 3.53.1 measured). Use nothing missing from 3.45; never assert the full text of `EXPLAIN QUERY PLAN`, only fragments such as `USING INDEX` or `SCAN`. Print `sqlite3.sqlite_version` where a lab's output depends on it.
- **Foreign keys are off by default** in every connection (`PRAGMA foreign_keys` is 0). Seeds and harnesses that need them turn them on explicitly; lab 3.3 teaches it.
- Run commands with `python -m pytest`, never bare `pytest`.
- Verify a lab: activate the virtual environment, check `python -c "import sys; print(sys.prefix)"` ends in `.venv`, then `python tools/verify.py --lab <ID>`. On a machine with Anaconda, Git Bash may silently leave the environment off `PATH` (see the StudyForge Python stack note).

## Upgrading the stack
1. Read the pytest changelog and the Python release notes (the `sqlite3` module and the bundled SQLite version); check Python support.
   For a new library, first apply StudyForge's checklist for choosing a dependency (`references/dependencies.md`) and run `pip-audit -r <file>`; record why in `docs/decisions.md`.
2. Change `requirements.txt`, `SETUP.md`, `SYLLABUS.md`, `TUTOR.md` (it names the versions), this file and the CI matrix.
3. Run `python tools/verify.py` on every supported Python; re-check every claim that quotes the old version (outputs, messages, query plans).
4. Commit `chore: upgrade <tool> to <version>`.

## Lessons
Stack-specific lessons live in `docs/lessons.md`; decisions in `docs/decisions.md`. Read both before building.
