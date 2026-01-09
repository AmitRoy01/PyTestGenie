"""Data models for test generation."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class TestGenerationResult:
    """Result from generating tests."""
    test_code: str
    error: Optional[str] = None
    method: Optional[str] = None  # 'pynguin' or 'ai'
