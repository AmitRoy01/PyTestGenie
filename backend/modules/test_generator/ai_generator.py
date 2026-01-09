"""AI-powered test generator using OpenAI via HuggingFace inference endpoints."""

import os
from typing import Optional
import ast
from openai import OpenAI
from .models import TestGenerationResult


def extract_test_code(ai_response: str) -> str:
    """Extract test code from AI response, handling both markdown and plain formats."""
    if "```" in ai_response:
        parts = ai_response.split("```")
        for i, part in enumerate(parts):
            if part.startswith("python"):
                return part[6:].strip()
            elif i % 2 == 1:
                return part.strip()
    return ai_response.strip()


def format_prompt(code: str) -> str:
    """Format the prompt for the AI model."""
    return f"""Generate Python unit tests for the following code using pytest. Include assertions to verify the code's behavior. Make the tests comprehensive but practical. Here's the code to test:

```python
{code}
```

Requirements:
1. Use pytest fixtures where appropriate
2. Include docstrings explaining each test's purpose
3. Use descriptive test names
4. Test both valid and invalid inputs
5. Add type hints to test functions
6. Include necessary imports

Return ONLY the test code, no explanations."""


class AITestGenerator:
    """Generates unit tests using OpenAI's API via HuggingFace."""
    
    def __init__(self, hf_token: Optional[str] = None):
        """Initialize the generator with optional HuggingFace token."""
        self.hf_token = hf_token or os.getenv("HF_TOKEN")
        if not self.hf_token:
            raise ValueError("HuggingFace token not found. Set HF_TOKEN environment variable.")
        
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=self.hf_token
        )
    
    def generate_tests(self, code: str) -> TestGenerationResult:
        """Generate unit tests for the given Python code."""
        try:
            # Validate the input code is valid Python
            ast.parse(code)
            
            # Generate tests using OpenAI
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-20b:groq",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python testing expert. Generate comprehensive pytest unit tests."
                    },
                    {
                        "role": "user",
                        "content": format_prompt(code)
                    }
                ],
                temperature=0.7
            )
            
            # Extract the test code from the response
            raw_response = completion.choices[0].message.content
            test_code = extract_test_code(raw_response)
            
            # Validate the generated test code is valid Python
            ast.parse(test_code)
            
            return TestGenerationResult(test_code=test_code, method='ai')
            
        except Exception as e:
            return TestGenerationResult(
                test_code="",
                error=f"Error generating tests: {str(e)}",
                method='ai'
            )
