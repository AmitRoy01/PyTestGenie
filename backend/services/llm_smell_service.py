"""LLM-based test smell detection service using Ollama and HuggingFace."""

import os
import json
import re
import shutil
import subprocess
import threading
import time
from openai import OpenAI

# Configuration (same env vars as refactoring)
HUGGINGFACE_API_KEY = os.getenv("HF_TOKEN", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Supported models
AVAILABLE_MODELS = {
    "ollama": [
        {"name": "Llama 3.2", "model_id": "llama3.2"},
    ],
    "huggingface": [
        {"name": "Mistral 7B Instruct v0.2", "model_id": "mistralai/Mistral-7B-Instruct-v0.2"},
        {"name": "GPT-OSS 20B", "model_id": "openai/gpt-oss-20b:groq"},
    ],
}

# ------------------------------------------------------------------
# Test smell catalogue with brief definitions so the LLM knows what
# to look for (mirrors the refactoring SMELL_DEFINITIONS dict).
# ------------------------------------------------------------------
SMELL_CATALOGUE = """
1. Assertion Roulette – Multiple assertions in one test without descriptive messages.
2. Conditional Test Logic – Test method contains if/switch/for/while control flow.
3. Exception Handling – Test method manually catches/throws exceptions instead of assertThrows.
4. Redundant Print – Test method contains print() calls that serve no assertion purpose.
5. Sleepy Test – Test method calls time.sleep() or any sleep/wait function.
6. Unknown Test – Test method has no assertions and no clear purpose.
7. Verbose Test – Excessively long test method (>20 lines) mixing setup, execution, and assertions.
8. Verifying in Setup – setUp / setUpClass method contains assertion calls.
9. Non-Functional Statement – Dead code, useless assignments, or commented-out code blocks that litter the test.
10. Undefined Test – Test method is defined but has an empty body (only pass or ...).
11. Magic Number Test – Assertion uses unexplained numeric / string literals.
12. Duplicate Assert – Same assertion with identical arguments appears more than once.
"""

# ------------------------------------------------------------------
# Helpers (mirror refactoring.py)
# ------------------------------------------------------------------

def _ensure_ollama() -> bool:
    return shutil.which("ollama") is not None


def _start_ollama() -> None:
    def _run():
        os.environ["OLLAMA_HOST"] = "0.0.0.0:11434"
        os.environ["OLLAMA_ORIGINS"] = "*"
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    threading.Thread(target=_run, daemon=True).start()
    time.sleep(2)


def get_llm_client(model_type: str, model_name: str):
    """Return (OpenAI-compatible client, effective_model_name). Same logic as refactoring."""
    if model_type == "ollama":
        if not _ensure_ollama():
            raise Exception("Ollama CLI not found. Please install from https://ollama.com")
        _start_ollama()
        try:
            subprocess.run(
                ["ollama", "pull", model_name],
                check=True, timeout=300,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except Exception as e:
            print(f"Warning: Could not pull model {model_name}: {e}")
        return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"), model_name

    elif model_type == "huggingface":
        os.environ["HF_TOKEN"] = HUGGINGFACE_API_KEY
        if not model_name:
            model_name = "mistralai/Mistral-7B-Instruct-v0.2"
        return OpenAI(base_url="https://router.huggingface.co/v1", api_key=HUGGINGFACE_API_KEY), model_name

    else:
        raise Exception("Invalid model_type. Use 'ollama' or 'huggingface'")


# ------------------------------------------------------------------
# Prompt building
# ------------------------------------------------------------------

def _build_detection_prompt(code: str, filename: str) -> str:
    return f"""You are an expert software testing engineer specializing in test code quality analysis.

Below is a catalogue of Python test smells you must detect:
{SMELL_CATALOGUE}

Analyze the following Python test file named "{filename}" and identify ALL test smell occurrences.

For EVERY smell found return a JSON array (and nothing else) where each element has:
  - "type"       : exact smell name from the catalogue above
  - "method"     : name of the test method (or class) where the smell occurs
  - "explanation": a clear explanation (2-4 sentences) of WHY this is a smell in this specific method.
                   Quote the exact problematic lines of code from the method using backtick formatting,
                   then explain what rule is violated and how the developer should fix it.

If NO smells are found, return an empty JSON array: []

Important rules:
- Output ONLY the JSON array, no markdown fences, no explanation text outside the array.
- Be precise: report only real smells, not false positives.
- In "explanation", always include a short quoted code snippet showing the problematic code.

Python test code:
```python
{code}
```"""


# ------------------------------------------------------------------
# Main detection function
# ------------------------------------------------------------------

def detect_smells_with_llm(
    code: str,
    filename: str,
    model_type: str = "ollama",
    model_name: str = "llama3.2",
    temperature: float = 0.2,
) -> dict:
    """
    Detect test smells in *code* using the specified LLM.

    Returns:
        {
          "success": bool,
          "smells": [{"type": str, "method": str, "lines": [int, ...]}, ...],
          "total_smells": int,
          "model_used": str,
          "error": str | None,
        }
    """
    try:
        client, effective_model = get_llm_client(model_type, model_name)
        prompt = _build_detection_prompt(code, filename)

        print(f"[LLM Smell Detector] model_type={model_type} model={effective_model}")

        completion = client.chat.completions.create(
            model=effective_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=4096,
        )
        raw = completion.choices[0].message.content or ""
        print(f"[LLM Smell Detector] Raw response length: {len(raw)}")

        smells = _parse_llm_response(raw)

        return {
            "success": True,
            "smells": smells,
            "total_smells": len(smells),
            "model_used": effective_model,
            "error": None,
        }

    except Exception as exc:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "smells": [],
            "total_smells": 0,
            "model_used": model_name,
            "error": str(exc),
        }


# ------------------------------------------------------------------
# Response parser – robust against common LLM formatting quirks
# ------------------------------------------------------------------

def _parse_llm_response(raw: str) -> list:
    """Extract the JSON array from the LLM response, tolerating markdown fences."""
    text = raw.strip()

    # Strip markdown code fences if present (```json ... ``` or ``` ... ```)
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    # Attempt direct parse
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return _normalise_smells(data)
    except json.JSONDecodeError:
        pass

    # Try to extract first JSON array with a regex fallback
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                return _normalise_smells(data)
        except json.JSONDecodeError:
            pass

    print(f"[LLM Smell Detector] Could not parse response as JSON array. Raw:\n{raw[:500]}")
    return []


def _normalise_smells(raw_list: list) -> list:
    """Ensure each entry has type, method, and explanation."""
    result = []
    for item in raw_list:
        if not isinstance(item, dict):
            continue
        smell_type = str(item.get("type", item.get("smell_type", item.get("smell", "Unknown")))).strip()
        method = str(item.get("method", item.get("function", item.get("test_method", "unknown")))).strip()
        explanation = str(item.get("explanation", item.get("reason", item.get("description", "")))).strip()
        result.append({"type": smell_type, "method": method, "explanation": explanation})
    return result
