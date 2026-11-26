"""The reference is done when the acceptance tests pass against its queries.

This test runs ../../acceptance with --queries=../queries, so the
verifier and the CI check the reference with the same tests a learner runs.
"""
import subprocess
import sys
from pathlib import Path

REFERENCE = Path(__file__).resolve().parent.parent
ACCEPTANCE = REFERENCE.parent / "acceptance"


def test_acceptance_passes_against_the_reference():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--queries={REFERENCE / 'queries'}"],
        cwd=ACCEPTANCE, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, output  # 5 would mean no test ran
    assert "7 passed" in output, output
