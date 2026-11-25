# Lessons

Lessons from building and reviewing the labs of this repository. Read them before building the next lab. Lessons that would help any study path are proposed upstream to StudyForge.

<!-- studyforge: Group by lab or by block. Each lesson: what happened, what was learned, how to apply it from now on. Keep it to facts that were run, not guesses. -->

## Lab 1.1
- **The `python -m sqlite3` console differs by Python version.** `.help` prints a command list only in 3.15 (3.12–3.14: "Enter SQL code and press enter."). An unknown dot command such as `.tables` errors in 3.13+ but in 3.12 is buffered as SQL until a `;`. Quote both when a lab touches it, and read `Lib/sqlite3/__main__.py` of each version instead of guessing.
- **Piping input into the console from PowerShell 5.1 breaks the first line** (the first command was not recognized as `.help`); piping from Bash did not. Drive console sessions from Bash, or start them with a harmless SQL line, when verifying.
- **Opening a misspelled file silently creates a 0-byte database**, in every version measured (3.12, 3.15, SQLite 3.45.3). It is the most likely "my data is gone" report from learners: first ask for `pwd` and the file size.
- **On Windows a database file open in a console cannot be deleted or rebuilt** (`PermissionError: [WinError 32]`, message in the Windows locale). Cleanup steps say `.quit` first.
- **With Python 3.12, output to a pipe uses cp1252 on Windows**, so accents come out garbled when the console's output is captured (3.15 defaults to UTF-8). In a PowerShell window they display correctly. Tests that run the console set `PYTHONIOENCODING=utf-8`.
- **In Git Bash on a machine with Anaconda, activating the venv left Anaconda's Python in charge** (3.12.7, SQLite 3.45.3), exactly as `SETUP.md` warns. Verify with `sys.prefix` every time.
