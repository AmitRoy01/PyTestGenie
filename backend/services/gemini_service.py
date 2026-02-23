import os
from typing import List, Dict, Tuple

from config.settings import Config

try:
    import google.genai as genai
    from google.genai.types import GenerateContentResponse
except ImportError:
    genai = None

from .explanation_fallback import rule_based_explanation


class GeminiClient:
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.model_name = model_name or Config.GEMINI_MODEL
        self.enabled = bool(self.api_key) and genai is not None
        self._client = None
        if self.enabled:
            # Use new google-genai API
            self._client = genai.Client(api_key=self.api_key)

    def explain_smell(self, code_context: str, smell_type: str, method_name: str, lines: List[int]) -> str | None:
        if not self.enabled:
            return None

        prompt = (
            "You are an expert in unit testing and test code quality. "
            "Given the following Python test code context and a detected test smell, "
            "explain clearly why this code likely exhibits the specified test smell. "
            "Reference the provided line numbers and method name, and suggest concrete, concise improvements. "
            "Keep the explanation under 160 words, structured with a short reason and a short fix.\n\n"
            f"Smell: {smell_type}\n"
            f"Method: {method_name}\n"
            f"Lines: {lines}\n\n"
            "Python test code context:\n"
            f"""{code_context}"""
        )
        try:
            # Use new google-genai API: client.models.generate_content()
            resp = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            # New API returns response with text attribute
            text = getattr(resp, "text", None)
            if text:
                return text.strip()
            return None
        except Exception as e:
            # On 429 or other failures, return None and let callers fallback
            return None


def load_code_context(filepath: str, lines: List[int], window: int = 3) -> str:
    """Extract a small context window around the given lines from a file."""
    if not os.path.exists(filepath):
        return "(File not found for context)"
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.readlines()
        spans: List[Tuple[int, int]] = []
        for ln in lines:
            start = max(1, ln - window)
            end = min(len(content), ln + window)
            spans.append((start, end))
        # Merge overlapping spans
        spans.sort()
        merged: List[Tuple[int, int]] = []
        for s, e in spans:
            if not merged or s > merged[-1][1] + 1:
                merged.append((s, e))
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        # Build context with line numbers
        ctx_lines = []
        for s, e in merged:
            for i in range(s, e + 1):
                ctx_lines.append(f"{i:>4}: {content[i-1].rstrip()}\n")
        return "".join(ctx_lines)
    except Exception:
        return "(Error reading code context)"


def generate_explanations_for_logs(project_path: str, logs: List) -> Dict[Tuple[str, str, Tuple[int, ...]], str]:
    """Generate Gemini explanations for each smell occurrence in logs.
    Returns a dict keyed by (project_path, method_name, tuple(lines)).
    """
    client = GeminiClient()
    explanations: Dict[Tuple[str, str, Tuple[int, ...]], str] = {}
    if not logs:
        return explanations
    for log in logs:
        # Each log has attributes: test_smell_type, method_name, lines
        key = (project_path, getattr(log, "method_name", ""), tuple(getattr(log, "lines", [])))
        code_ctx = load_code_context(project_path, getattr(log, "lines", []))
        explanation = client.explain_smell(code_ctx, getattr(log, "test_smell_type", ""), getattr(log, "method_name", ""), getattr(log, "lines", []))
        if not explanation:
            explanation = rule_based_explanation(getattr(log, "test_smell_type", ""), getattr(log, "method_name", ""), getattr(log, "lines", []))
        explanations[key] = explanation
    return explanations


def _format_code_with_line_numbers(code_text: str) -> List[str]:
    lines = code_text.splitlines()
    return [f"{i+1:>4}: {line}\n" for i, line in enumerate(lines)]


def generate_explanations_for_logs_from_code(code_text: str, virtual_name: str, logs: List) -> Dict[Tuple[str, str, Tuple[int, ...]], str]:
    """Generate explanations using provided code text (not relying on file path)."""
    client = GeminiClient()
    explanations: Dict[Tuple[str, str, Tuple[int, ...]], str] = {}
    numbered = _format_code_with_line_numbers(code_text)
    if not logs:
        return explanations
    for log in logs:
        key = (virtual_name, getattr(log, "method_name", ""), tuple(getattr(log, "lines", [])))
        # Build context window based on lines from the numbered code
        ctx_lines: List[str] = []
        for ln in getattr(log, "lines", []):
            start = max(1, ln - 3)
            end = ln + 3
            for i in range(start, end + 1):
                if 1 <= i <= len(numbered):
                    ctx_lines.append(numbered[i-1])
        code_ctx = "".join(ctx_lines) if ctx_lines else "".join(numbered[:min(30, len(numbered))])
        explanation = client.explain_smell(
            code_ctx,
            getattr(log, "test_smell_type", ""),
            getattr(log, "method_name", ""),
            getattr(log, "lines", []),
        )
        if not explanation:
            explanation = rule_based_explanation(getattr(log, "test_smell_type", ""), getattr(log, "method_name", ""), getattr(log, "lines", []))
        explanations[key] = explanation
    return explanations
