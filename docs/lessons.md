# Lessons

Measured rules from building and reviewing the labs; read them before building one. A lab in parentheses marks where a rule was learned. Lessons useful to any study path go upstream to StudyForge.

<!-- studyforge: Group by topic, one imperative rule per bullet. Merge repeats; drop a rule once a tool, the harness or AGENTS.md enforces it. -->

## Test data and variant batteries
- A wrong query returns other rows, never an error, so the data decides whether a test can see it. Before committing a challenge, run a battery of beginner variants (wrong and right-but-different; 29 to 67 per lab so far) against the solution: every wrong one must fail only its own test, every right one must pass.
- Run batteries with plain `sqlite3` and keep pytest for the prediction outputs and the final check: Anaconda's pytest is about ten times slower per run.
- Put data on every edge a test checks: a value on each limit (1.3: rents 1200, 1800, 2000), another capitalization, the searched text at the start, middle and end, a name that starts like another (`San …` and `Santiago de Surco`), a `NULL` and a non-`NULL` row on each side of each rule, and a `NULL` next to the `0` or `''` it could be confused with (1.4).
- For every rounding a test checks, run `ROUND(x, n − 1)`, `ROUND(x, n + 1)`, `ROUND(x)` and no rounding as mutations, and pick data where each one changes at least one row (1.2: the alfajor at 3.7). Elsewhere avoid floating-point noise: measure that each subtraction a test compares unrounded gives the exact literal.
- SQLite returns tied rows in insertion order (3.45.3 and 3.53.1), so a missing tiebreak passes when the insertion order already matches it. Store every tied pair opposite to its tiebreak, and run the other tasks' tiebreaks and plausible ones (`title`, `price`, `id`) as mutations of every ordering test.
- A `DISTINCT` fix passes when no two values in a group are equal: to show that `SUM(DISTINCT)` does not undo a fan-out, seed two equal values on different rows of one group (2.5: a second 600 job at Agro Norte).
- Break coincidences: a wrong query that is right on every row passes. A wrong join key must match on some rows and not others (2.2: `a.id = c.id` gets application 1 right), and in a project each rule needs a row that breaks it in every query that uses it (1.P: the only `NULL` stock belonged to an active product, so a missing parenthesis passed).
- A rule with two sides needs a row that has both: a customer with a sale and a cancelled order (2.P: order 111) separates "has no sale" from "has a non-sale order or none", and a quantity above 1 on the page under test separates `SUM(quantity)` from `COUNT(*)`.
- A page test only sees its page: make the requested page the last, short one, so one extra or missing row changes it.
- When the tests cannot tell a right-but-worse answer apart (`substr(x, 0, 4)`, a `NOT IN` list instead of a pattern, a double-quoted value), accept it and say in ✔️ why it passed and what to write instead.

## Predictions and spoilers
- After a 🔮, the step that runs the tests says "compara lo que muestra con tu predicción", never "lee el fallo" or "las filas que sobran": with a yes/no prediction, the word "fallo" answers it. The next step states the goal ("Deja en el archivo una consulta que …"), never "Corrige …" nor the fix ("con paréntesis", "redondea").
- When a prediction puts a query in the task file, the next step says "Reemplaza la consulta de la predicción …", not "Escribe": two statements in one file fail. A step that changes a solved query says "En esa misma consulta, cambia … por …".
- Before committing, check every step that follows a 🔮 against the two rules above, one by one (missed in all four tasks of 1.4).
- Name tests after the task's goal, not after its trap: the first run lists every test in `FAILED` before any prediction (1.3: `test_districts_not_starting_with_the_word_san` gave the space away).
- When a prediction offers "an error" as an option, search everything above it for "error" and "avisa": a general statement answers it (1.3, 2.2).
- Read every file the README links before a prediction, not only the README: a comment in `seed.sql` answered one (2.1).
- Run every Concepts example and read its raw output before choosing what to show: an output can answer a later prediction (1.2: `1200 * 3.7413` prints `4489.5599999999995`).
- Do not state in Concepts what a prediction asks; give the tools there and explain the behavior in ✔️.
- Keep every Concepts sentence true on the trap's data: "basta preguntar por una de ellas" (any column of the right table) was false for a nullable column and would have taught the task 3 trap as a rule (2.3); name the column the example uses instead.
- Do not name the rows that differ in a prediction; ask for a count (1.4).
- Read the objectives and the captions of the data tables as part of "above the prediction": a caption ("`salary_usd` is a whole number") or an objective ("recognize when dividing integers loses the decimals") answered one (2.4).
- Make prediction queries return the task's columns, or the harness stops at "las columnas no coinciden" before showing the rows; keep the trap in the one expression the prediction is about.
- Put the 🔮 before the command that reveals it, even a command that only opens something (`Connected to …`).

## SQLite traps to plan around
Measured the same in SQLite 3.45.3 and 3.53.1.
- An unknown double-quoted name becomes text (`"nmae"`, `WHERE district = "Miraflores"` passes), an alias in single quotes works and an alias works in `WHERE`; PostgreSQL rejects all three. The harness cannot see quotes.
- `STRFTIME` returns text: `STRFTIME('%Y', d) = 2026` is false with no error.
- A scalar subquery that returns several rows gives its first row, no error (2.6: PostgreSQL rejects it); an unqualified column in a correlated subquery resolves to the inner table first (`company_id = company_id` is always true).
- `'x' NOT IN ('a', NULL)` is `NULL`; `100 / 0` is `NULL` with no error; integer division truncates (owned by 2.4).
- `LIKE` folds case only for ASCII letters, and `LOWER` changes only ASCII letters; text sorts by code point.
- A foreign key is not checked unless `PRAGMA foreign_keys` is on: an `INSERT` that breaks one prints nothing.
- The `python -m sqlite3` console commits each statement at once: a guide that inserts rows says how to rebuild the database (`python build_db.py`).

## Versions and quoted output
- Run every quoted message and output on every Python at hand (`uv python list --only-installed`: 3.12 to 3.15 and Anaconda), not only the CI ones. Quote only the stable start of a version-dependent message (`Error: unknown command`), or each version separately.
- Quote the error of the exact statement the README shows, not of a similar one (1.5: `near "0"` came from another statement).
- The `python -m sqlite3` console differs by version: `.help` lists commands only in 3.15; an unknown dot command errors in 3.13+ and in 3.12 waits for a `;`. Read each version's `Lib/sqlite3/__main__.py`, do not guess. Its banner has four lines and says CTRL-Z on Windows: quote it whole and gloss each line.
- The version line of ✔️ (at the start of 🧪 in explorations) says exactly what ran, never copied from another lab: "Verificado en Windows 11, en PowerShell 5.1, con Python … y con Python 3.12.7 de Anaconda (SQLite 3.45.3)." Git Bash enters only if a command behaves differently there and was run.

## Windows, shells and encodings
- Check encodings in a shell started with `powershell -NoProfile`: the agent's profile sets UTF-8 and hides that stock PowerShell 5.1 writes `>` in UTF-16 with a BOM, `Set-Content` writes CRLF (harmless with `.gitattributes`), and `Get-Content` garbles UTF-8.
- Python 3.12 to 3.14 on Windows write cp1252 to a pipe or file (3.15 writes UTF-8). Tests that run the console set `PYTHONIOENCODING=utf-8`; the harness's `conftest.py` handles pytest.
- Drive console sessions from Bash, or start them with a harmless SQL line: piping from PowerShell 5.1 breaks the first line.
- A database open in a console cannot be deleted or rebuilt on Windows (`WinError 32`): cleanup steps say `.quit` first.
- Opening a misspelled file silently creates a 0-byte database; for "my data is gone", ask first for `pwd` and the file size.
- A step that depends on a file size gives `ls` for PowerShell (`Length` column) and `ls -l` for Bash; plain `ls` in Bash shows names only.
- The wrong-environment failure in Git Bash depends on the inherited `PATH`, not on Anaconda alone. Tell learners to check `sys.prefix`, never that "Anaconda breaks Git Bash"; the prompt `(.venv)` and the pytest version prove nothing. The signal learners can see is a `plugins:` line or `warnings` in pytest's output.
- In PowerShell, `[IO.File]` methods resolve relative paths against the process's starting folder, not the one `cd` moved to: an edit with `[IO.File]::ReadAllText('SYLLABUS.md')` after `cd` read nothing and wrote an empty file in another repository. Use full paths, or `Get-Content`/`Set-Content -Encoding utf8`, or edit from Python.
- In this agent's Git Bash, `cygpath` is Anaconda's (write Windows paths by hand), and a quoted heredoc turned `\n` in Python source into a newline (write files with escapes through a file-writing tool).
- Make a script that rewrites many READMEs safe to run twice (it skips a file already in the new shape) and run it with `PYTHONIOENCODING=utf-8`: in the 1.8.0 upgrade, printing a 👀 in cp1252 crashed it after it had written the first file, and a rerun of a non-idempotent move would have moved the solution line into ✔️.

## Harness and pytest
- Call `pytest.fail` outside the `except` block, or pytest prints the original exception above the learner's message.
- A `pytest.fail` in a session fixture repeats as an ERROR in every test; stop once with `pytest.exit` from `pytest_sessionstart`.
- A project with a fixed "today" says so next to the date, and the harness reminds when a query contains `'now'`. `DATE(col) BETWEEN … AND today` keeps today's rows; only the raw date-time column loses them.

## Writing for beginners
- Gloss every new word or file the learner sees, even one they do not use (a pragma, `pyproject.toml`, the console banner): one line ("no lo toques, es para las pruebas") is enough.
- Teach only what a task uses: a flag shown only in the command dissection is not taught.
- Say whether to run the Concepts examples when the lab never opens the console.
- Explain each error a task provokes on purpose in its lab; put common syntax slips seen from learners in the hints, after the task (`IN` without parentheses, `_` read as a space).
- Make self-assessment answers respect the rules the lab teaches (`'abcd' LIKE 'A___'` is 1 in SQLite).
- Say "hoja de cálculo", not "planilla" (payroll in Peru).

## Links
- Open every external link with its anchor before committing: the repository checks validate only internal anchors (1.6 guessed `lang_expr.html#operators`).
- Link only documentation that teaches the lab's topic.
- dev.mysql.com answers `curl` with 403 (2.7): a MySQL claim needs another checked source, or leave it out; do not write it from memory.
