import os
import re
from typing import Optional, List, Dict, Tuple
import ast
from pathlib import Path
from openai import OpenAI
from .models import TestGenerationResult


def extract_imports(code: str) -> List[Tuple[str, str]]:
    """Extract import statements from Python code.
    
    Returns:
        List of tuples (import_type, module_name)
        import_type: 'import' or 'from'
        module_name: the module being imported
    """
    imports = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(('import', alias.name.split('.')[0]))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(('from', node.module.split('.')[0]))
    except:
        # Fallback to regex if AST parsing fails
        import_pattern = r'^(?:from\s+(\w+)|import\s+(\w+))'
        for line in code.split('\n'):
            match = re.match(import_pattern, line.strip())
            if match:
                module = match.group(1) or match.group(2)
                imports.append(('from' if match.group(1) else 'import', module))
    
    return imports


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


def format_prompt(code: str, dependencies: Optional[Dict[str, str]] = None) -> str:
    """Format the prompt for the AI model.
    
    Args:
        code: The main code to test
        dependencies: Optional dict of {module_name: module_code} for imported modules
    """
    prompt = """Generate Python unit tests for the following code using pytest. Include assertions to verify the code's behavior. Make the tests comprehensive but practical.

"""
    
    # Add dependency context if available
    if dependencies:
        prompt += "**Project Context - Imported Modules:**\n\n"
        for module_name, module_code in dependencies.items():
            prompt += f"Module: {module_name}.py\n```python\n{module_code}\n```\n\n"
    
    prompt += f"""**Main Code to Test:**

```python
{code}
```

**Requirements:**
1. Use pytest fixtures where appropriate
2. Include docstrings explaining each test's purpose
3. Use descriptive test names
4. Test both valid and invalid inputs
5. Add type hints to test functions
6. Include necessary imports (considering the modules shown above)
7. Mock or handle dependencies appropriately

Return ONLY the test code, no explanations."""
    
    return prompt


class AITestGenerator:
    """Generates unit tests using AI models (GPT-OSS via HuggingFace or Llama 3.2 locally)."""
    
    # Supported models configuration
    MODELS = {
        "gpt-oss": {
            "name": "GPT-OSS 20B",
            "model_id": "openai/gpt-oss-20b:groq",
            "base_url": "https://router.huggingface.co/v1",
            "requires_hf_token": True
        },
        "llama-3.2": {
            "name": "Llama 3.2",
            "model_id": "llama3.2",
            "base_url": "http://localhost:11434/v1",
            "requires_hf_token": False
        }
    }
    
    def __init__(self, model_name: str = "gpt-oss", hf_token: Optional[str] = None, llama_url: Optional[str] = None):
        """Initialize the generator with specified model.
        
        Args:
            model_name: Model to use ('gpt-oss' or 'llama-3.2')
            hf_token: HuggingFace token (required for gpt-oss)
            llama_url: Llama server URL (optional, defaults to localhost:11434)
        """
        if model_name not in self.MODELS:
            raise ValueError(f"Unsupported model: {model_name}. Supported models: {list(self.MODELS.keys())}")
        
        self.model_name = model_name
        self.model_config = self.MODELS[model_name]
        
        # Set up API key and base URL based on model type
        if self.model_config["requires_hf_token"]:
            self.api_key = hf_token or os.getenv("HF_TOKEN")
            if not self.api_key:
                raise ValueError("HuggingFace token not found. Set HF_TOKEN environment variable.")
            base_url = self.model_config["base_url"]
        else:
            # For Llama, use dummy key (required by OpenAI client but not used)
            self.api_key = "ollama"
            base_url = llama_url or os.getenv("LLAMA_API_URL", self.model_config["base_url"])
        
        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key
        )
    
    def generate_tests(self, code: str, project_path: Optional[str] = None) -> TestGenerationResult:
        """Generate unit tests for the given Python code.
        
        Args:
            code: The Python code to generate tests for
            project_path: Optional path to project directory for resolving imports
        """
        try:
            # Validate the input code is valid Python
            ast.parse(code)
            
            # Build dependency context if project path is provided
            dependencies = None
            if project_path:
                dependencies = self._resolve_dependencies(code, project_path)
            
            # Generate tests using the selected model
            completion = self.client.chat.completions.create(
                model=self.model_config["model_id"],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python testing expert. Generate comprehensive pytest unit tests. When dependencies are provided, understand their functionality and mock them appropriately in tests."
                    },
                    {
                        "role": "user",
                        "content": format_prompt(code, dependencies)
                    }
                ],
                temperature=0.7
            )
            
            # Extract the test code from the response
            raw_response = completion.choices[0].message.content
            test_code = extract_test_code(raw_response)
            
            # Validate the generated test code is valid Python
            ast.parse(test_code)
            
            return TestGenerationResult(test_code=test_code, method=f'ai-{self.model_name}')
            
        except Exception as e:
            return TestGenerationResult(
                test_code="",
                error=f"Error generating tests with {self.model_config['name']}: {str(e)}",
                method=f'ai-{self.model_name}'
            )
    
    def _resolve_dependencies(self, code: str, project_path: str) -> Dict[str, str]:
        """Resolve and read imported modules from the project.
        
        Args:
            code: The main code being tested
            project_path: Path to the project directory
        
        Returns:
            Dictionary mapping module names to their source code
        """
        dependencies = {}
        imports = extract_imports(code)
        project_dir = Path(project_path)
        
        for import_type, module_name in imports:
            # Skip standard library and third-party imports
            if module_name in ['os', 'sys', 'json', 'time', 'datetime', 'math', 're', 
                              'typing', 'pathlib', 'collections', 'itertools', 'functools',
                              'unittest', 'pytest', 'numpy', 'pandas', 'requests', 'flask']:
                continue
            
            # Try to find the module in the project
            module_path = project_dir / f"{module_name}.py"
            if module_path.exists():
                try:
                    with open(module_path, 'r', encoding='utf-8', errors='replace') as f:
                        dependencies[module_name] = f.read()
                except Exception:
                    pass
            else:
                # Check if it's a package
                package_init = project_dir / module_name / "__init__.py"
                if package_init.exists():
                    try:
                        with open(package_init, 'r', encoding='utf-8', errors='replace') as f:
                            dependencies[module_name] = f.read()
                    except Exception:
                        pass
        
        return dependencies
