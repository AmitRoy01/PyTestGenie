from typing import List

TEMPLATE = {
    "Conditional Test Logic": (
        "Reason: The test includes control flow (e.g., if/for/while) in `{method}` around lines {lines}. Conditional logic can hide assertion paths and make tests harder to reason about and maintain.\n"
        "Fix: Extract the branching into the production code or helper functions and assert separate deterministic scenarios. Prefer parameterized tests over inline branching."
    ),
    "Exception Handling": (
        "Reason: The test manually uses try/except in `{method}` at lines {lines}, which can swallow failures or introduce false positives.\n"
        "Fix: Use testing frameworks' exception assertions (e.g., pytest `raises`, unittest `assertRaises`) to explicitly validate exceptions without manual try/except."
    ),
    "Redundant Print": (
        "Reason: Print statements appear in `{method}` at lines {lines}. Printing adds noise, hides intent, and doesn't validate behavior.\n"
        "Fix: Remove prints and assert on returned values, state changes, or logs via a logger/handler if output visibility is required."
    ),
    "Sleepy Test": (
        "Reason: Sleep or waits are used in `{method}` at lines {lines}. Time-based waiting makes tests flaky and slow.\n"
        "Fix: Replace sleeps with synchronization primitives (events, conditions) or deterministic hooks; in async flows, await signals instead of fixed delays."
    ),
    "Unknown Test": (
        "Reason: `{method}` at line {first_line} looks like a test but contains no assertions. This makes the test non-verifying.\n"
        "Fix: Add assertions for expected outcomes, or demote this to a helper/fixture."
    ),
    "Verbose Test": (
        "Reason: `{method}` spans many lines ({range_text}), indicating multiple responsibilities or setup inline.\n"
        "Fix: Refactor into smaller focused tests, move setup to fixtures/factories, and keep each test validating one behavior."
    ),
    "Programming Paradigms Blend": (
        "Reason: The file mixes procedural code and classes, which can complicate test structure.\n"
        "Fix: Choose one style per file: keep tests as functions with fixtures or as methods under a test class; avoid mixing without need."
    ),
    "Verifying in Setup Method": (
        "Reason: Assertions appear in setup/teardown (`{method}`) at lines {lines}, hiding failures outside test boundaries.\n"
        "Fix: Move assertions into test bodies; setup/teardown should prepare/cleanup only."
    ),
    "Non-Functional Statement": (
        "Reason: `pass` statements were found in `{method}` at lines {lines} that do not belong to function signatures, indicating dead or placeholder code.\n"
        "Fix: Remove placeholders or implement meaningful checks; keep function bodies non-empty only if necessary."
    ),
    "Undefined Test": (
        "Reason: `{method}` contains assertions but is not named as a test. This may prevent discovery by the test runner.\n"
        "Fix: Rename to start with `test_` (pytest/unittest discovery) or register explicitly, ensuring the test is executed."
    ),
}


def rule_based_explanation(smell_type: str, method_name: str, lines: List[int]) -> str:
    tmpl = TEMPLATE.get(smell_type)
    if not tmpl:
        return (
            f"Reason: Detected '{smell_type}' in `{method_name}` at lines {lines}.\n"
            "Fix: Apply standard testing best practices to make assertions explicit, remove noise, and split responsibilities."
        )
    first_line = lines[0] if lines else "?"
    range_text = f"{lines[0]}–{lines[-1]}" if len(lines) >= 2 else str(first_line)
    text = tmpl.format(method=method_name, lines=lines, first_line=first_line, range_text=range_text)
    return text
