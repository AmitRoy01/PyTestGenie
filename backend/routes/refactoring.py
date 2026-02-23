"""Route handlers for test code refactoring using AI agents."""

from flask import Blueprint, request, jsonify
from typing import Optional
import os
import shutil
import subprocess
import threading
import time
from openai import OpenAI

refactoring_bp = Blueprint('refactoring', __name__)

# Configuration
HUGGINGFACE_API_KEY = os.getenv("HF_TOKEN", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Available models
AVAILABLE_MODELS = {
    "ollama": [
        {"name": "Llama 3.2", "model_id": "llama3.2"},
        {"name": "Phi 4", "model_id": "phi4"},
        {"name": "Mistral", "model_id": "mistral"},
        {"name": "CodeLlama", "model_id": "codellama"},
    ],
    "huggingface": [
        {"name": "Mistral 7B Instruct v0.2", "model_id": "mistralai/Mistral-7B-Instruct-v0.2"},
        {"name": "GPT-OSS 20B", "model_id": "openai/gpt-oss-20b:groq"},
    ]
}

# Smell definitions
SMELL_DEFINITIONS = {
    "Assertion Roulette": """
A test method contains more than one assertion statement without an explanation or message (parameter in the assertion method).
How to refactor?
Add a message to each assertion: Provide short, specific explanations so you know why an assertion fails.
""",
    "Magic Number Test": """
The Magic Number Test smell occurs when a test method contains an assertion with a numeric literal as an argument.
How to refactor?
Extract and initialize all magic numbers into constants or local variables with descriptive names.
""",
    "Duplicate Assert": """
The Duplicate Assert test smell occurs when a test method contains more than one assertion statement with the same parameters.
How to refactor?
If multiple assertions test different scenarios or states, split them into separate tests for clarity.
""",
    "Exception Handling": """
The Exception Handling test smell occurs when a test method contains either a throw statement or at least a catch clause.
How to refactor?
Use the testing framework's features (e.g., assertThrows) instead of manually catching or throwing exceptions.
""",
    "Conditional Test Logic": """
The Conditional Test Logic test smell occurs when a test method contains one or more control statements
(i.e if, switch, conditional expression, for, foreach and while statement).
How to refactor?
Create a dedicated test method for each condition.
""",
    "Missing Assertion": """
The Missing Assertion test smell occurs when a test method contains no assertions at all.
How to refactor?
Add assertions to verify expected outcomes, or convert the method to a helper/fixture if it's not meant to be a test.
""",
    "All": """
Refactor the test code to address all common test smells including:
1. Assertion Roulette - Add explanatory messages to all assertions
2. Magic Number Test - Extract numeric literals into named constants
3. Duplicate Assert - Remove or separate duplicate assertions
4. Exception Handling - Use framework features like assertThrows instead of try-catch
5. Conditional Test Logic - Split tests with conditionals into separate test methods
6. Missing Assertion - Add assertions to verify expected behavior

How to refactor?
Analyze the code for all the above smells and apply appropriate refactoring for each detected issue.
"""
}


def ensure_ollama() -> bool:
    """Check if Ollama is available."""
    return shutil.which("ollama") is not None


def start_ollama() -> None:
    """Run `ollama serve` in background if it is not already running."""
    def _run() -> None:
        os.environ["OLLAMA_HOST"] = "0.0.0.0:11434"
        os.environ["OLLAMA_ORIGINS"] = "*"
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    threading.Thread(target=_run, daemon=True).start()
    time.sleep(2)


def get_llm(model_type: str, model_name: str, temperature: float):
    """Get the appropriate LLM client based on model type."""
    if model_type == "ollama":
        if not ensure_ollama():
            raise Exception("Ollama CLI not found. Please install from https://ollama.com")
        
        start_ollama()
        
        # Pull model if not available
        try:
            print(f"Pulling Ollama model: {model_name}")
            subprocess.run(["ollama", "pull", model_name], 
                         check=True, timeout=300,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        except Exception as e:
            print(f"Warning: Could not pull model {model_name}: {e}")
        
        return OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Ollama doesn't need real API key
        ), model_name
    
    elif model_type == "huggingface":
        os.environ["HF_TOKEN"] = HUGGINGFACE_API_KEY
        # Default to a reliable model if not specified
        if not model_name:
            model_name = "mistralai/Mistral-7B-Instruct-v0.2"
            
        return OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HUGGINGFACE_API_KEY
        ), model_name
    
    else:
        raise Exception("Invalid model_type. Use 'ollama' or 'huggingface'")


# ========== SINGLE AGENT FUNCTIONS ==========

def build_single_agent_prompt(test_smell_name: str, test_smell_definition_and_refactoring: str, code: str) -> str:
    """Build prompt template for single agent refactoring."""
    return f"""
You are a coding assistant specializing in test code analysis and refactoring, with many years of experience.
{test_smell_definition_and_refactoring}

Your task:
Analyze the provided Python test code to identify and resolve occurrences of "{test_smell_name}".
If no such smell is present, return the original code unchanged. Ensure that the refactored test maintains the same behavior while eliminating the {test_smell_name}.
Finally, output only the final refactored code, ensuring it is valid Python code following pytest/unittest conventions and free of syntax errors, without providing any additional explanations or text.

Code to analyze:
{code}
"""


def invoke_llm(client: OpenAI, model_name: str, prompt: str, temperature: float) -> str:
    """Invoke LLM with OpenAI client."""
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM: {str(e)}")
        raise


def refactor_single_agent(
    client: OpenAI,
    model_name: str,
    code: str,
    smell_name: str,
    smell_definition: str,
    temperature: float = 0.6
) -> dict:
    """
    Single agent refactoring approach.
    
    Args:
        client: OpenAI client instance
        model_name: Name of the model to use
        code: Test code to analyze and refactor
        smell_name: Name of the test smell
        smell_definition: Definition and refactoring guidance for the smell
        temperature: LLM temperature setting
    
    Returns:
        dict with 'success', 'refactored_code', and optional 'error'
    """
    try:
        # Build prompt
        prompt = build_single_agent_prompt(smell_name, smell_definition, code)
        
        print(f"[Single Agent] Invoking LLM with model: {model_name}")
        print(f"[Single Agent] Analyzing code for smell: {smell_name}")
        
        # Invoke LLM
        refactored_code = invoke_llm(client, model_name, prompt, temperature)
        
        print(f"[Single Agent] LLM Response received")
        
        # Handle empty or invalid response
        if not refactored_code or refactored_code.strip() == "":
            print("[Single Agent] Warning: Empty response from LLM, returning original code")
            refactored_code = code
        
        return {
            "success": True,
            "refactored_code": refactored_code,
            "error": None
        }
    
    except Exception as e:
        print(f"[Single Agent] Error during refactoring: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "refactored_code": code,
            "error": str(e)
        }


# ========== MULTI AGENT FUNCTIONS ==========

def build_multi_agent_prompts(test_smell_name: str, test_smell_definition_and_refactoring: str) -> dict:
    """Build all prompt templates for multi-agent approach."""
    
    detect = f"""
You are a coding assistant with many years of experience that detects test smells.
{test_smell_definition_and_refactoring}

Your goal is to determine if the provided test code exhibits the test smell "{test_smell_name}".
{{code}}
Next I may give you further details.
{{agent_feedback}}
If the test code contains {test_smell_name}, respond with EXACTLY "YES" on the first line and explain why. Ignore code comments. If it does not contain, say EXACTLY "NO" on the first line and explain why not.
"""
    
    eval_detect = f"""
You are a coding expert reviewing the detection of a test smell. Consider the following test smell.
{test_smell_definition_and_refactoring}

A previous agent analyzed the following test code.
{{code}}
It gave the following answer.
{{agent_answer}}
Your goal is to evaluate if the previous detection by another agent is correct and justified. Ignore code comments.
If you do not agree, answer NO and explain what's wrong with it and what to correct.
If yes, just say YES.
"""
    
    refactor = f"""
You are a coding assistant specializing in test code analysis and refactoring, with many years of experience.

{test_smell_definition_and_refactoring}

Your task is as follows.
First analyze the provided Python test code to resolve test smell occurrences "{test_smell_name}". If there is no smell, output the original code unchanged.
Second ensure the test preserves the same behavior, but is free of {test_smell_name}.
Third output only the final refactored code, valid Python code.
Finally check the refactored version does not introduce syntax errors.

Provide only the final refactored code, with no additional explanation or text.
Code to analyze:
{{code}}

Next I may provide you further details.
{{reviewer_feedback}}
"""
    
    eval_refactor = f"""
You are a code reviewer specializing in test smells.
{test_smell_definition_and_refactoring}

Analyze the following code.
{{refactored_code}}

Your task is to check three conditions.
First check the code does not have the test smell {test_smell_name}.
Second verify the code follows Python testing best practices (pytest/unittest conventions).
Finally confirms the code does not have syntax errors.

If the code satisfy all conditons, respond with EXACTLY "YES" on the first line.
If not, respond with EXACTLY "NO" on the first line, then explain in one or two sentences why.

Let's think step by step.
"""
    
    return {
        "detect": detect,
        "eval_detect": eval_detect,
        "refactor": refactor,
        "eval_refactor": eval_refactor,
    }


def refactor_multi_agent(
    client: OpenAI,
    model_name: str,
    code: str,
    smell_name: str,
    smell_definition: str,
    temperature: float = 0.6,
    max_iters: int = 3
) -> dict:
    """
    Multi-agent refactoring approach with detection, evaluation, refactoring, and review phases.
    
    Args:
        client: OpenAI client instance
        model_name: Name of the model to use
        code: Test code to analyze and refactor
        smell_name: Name of the test smell
        smell_definition: Definition and refactoring guidance for the smell
        temperature: LLM temperature setting
        max_iters: Maximum iterations for detection and refactoring phases
    
    Returns:
        dict with 'success', 'refactored_code', 'detection_results', and optional 'error'
    """
    try:
        # Build prompts
        prompts = build_multi_agent_prompts(smell_name, smell_definition)
        
        detection_results = []
        explanation = ""
        confirmed = False
        
        print(f"[Multi-Agent] Starting detection phase with model: {model_name}")
        print(f"[Multi-Agent] Analyzing code for smell: {smell_name}")
        
        # PHASE 1: Detection phase (max iterations)
        for it in range(1, max_iters + 1):
            print(f"[Multi-Agent] Detection Iteration {it}/{max_iters}")
            
            # Agent 1: Detect smell
            detect_prompt = prompts["detect"].replace("{code}", code).replace("{agent_feedback}", explanation)
            r1 = invoke_llm(client, model_name, detect_prompt, temperature)
            
            # Agent 2: Evaluate detection
            eval_detect_prompt = prompts["eval_detect"].replace("{code}", code).replace("{agent_answer}", r1)
            r2 = invoke_llm(client, model_name, eval_detect_prompt, temperature)
            
            iteration_result = {
                "iteration": it,
                "phase": "detection",
                "detected_smell": "YES" if "yes" in r1.lower() else "NO",
                "agreed_with_detection": "YES" if "yes" in r2.lower() else "NO",
                "detection_response": r1,
                "evaluation_response": r2
            }
            detection_results.append(iteration_result)
            
            print(f"[Multi-Agent] Agent 1 (Detector) - Smell detected: {'YES' if 'yes' in r1.lower() else 'NO'}")
            print(f"[Multi-Agent] Agent 2 (Evaluator) - Agreed: {'YES' if 'yes' in r2.lower() else 'NO'}")
            
            if "yes" in r2.lower():
                confirmed = True
                explanation = r1
                print(f"[Multi-Agent] Detection confirmed in iteration {it}")
                break
            explanation = r1
        
        # Check if smell was confirmed
        if not confirmed:
            print("[Multi-Agent] Test smell not confirmed by evaluator. Skipping refactoring.")
            return {
                "success": True,
                "refactored_code": code,
                "detection_results": detection_results,
                "error": "Test smell not confirmed by evaluator"
            }
        
        if not "yes" in r1.lower():
            print("[Multi-Agent] Test smell not detected. Skipping refactoring.")
            return {
                "success": True,
                "refactored_code": code,
                "detection_results": detection_results,
                "error": "Test smell not detected"
            }
        
        # PHASE 2: Refactoring phase (max iterations)
        print(f"[Multi-Agent] Starting refactoring phase")
        current_code = code
        feedback = explanation
        final_refactored = code
        
        for it in range(1, max_iters + 1):
            print(f"[Multi-Agent] Refactoring Iteration {it}/{max_iters}")
            
            # Agent 3: Refactor code
            refactor_prompt = prompts["refactor"].replace("{code}", current_code).replace("{reviewer_feedback}", feedback)
            ref = invoke_llm(client, model_name, refactor_prompt, temperature)
            
            # Agent 4: Evaluate refactoring
            eval_refactor_prompt = prompts["eval_refactor"].replace("{refactored_code}", ref)
            chk = invoke_llm(client, model_name, eval_refactor_prompt, temperature)
            
            ok = "yes" in chk.lower()
            
            refactor_result = {
                "iteration": it,
                "phase": "refactor",
                "refactored_code": ref,
                "evaluation": chk,
                "approved": "YES" if ok else "NO",
                "smell_removed": "YES" if ok else "NO"
            }
            detection_results.append(refactor_result)
            
            print(f"[Multi-Agent] Agent 3 (Refactorer) - Code refactored")
            print(f"[Multi-Agent] Agent 4 (Reviewer) - Approved: {'YES' if ok else 'NO'}")
            
            if ok:
                final_refactored = ref
                print(f"[Multi-Agent] Refactoring approved in iteration {it}")
                break
            
            feedback = "\n".join(chk.splitlines()[1:]) or "No explanation"
            current_code = ref
            final_refactored = ref
        
        print("[Multi-Agent] Refactoring complete")
        
        return {
            "success": True,
            "refactored_code": final_refactored,
            "detection_results": detection_results,
            "error": None
        }
    
    except Exception as e:
        print(f"[Multi-Agent] Error during refactoring: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "refactored_code": code,
            "detection_results": detection_results if 'detection_results' in locals() else [],
            "error": str(e)
        }


# ========== ROUTES ==========

@refactoring_bp.route('/models', methods=['GET'])
def get_models():
    """Get available models for each provider."""
    return jsonify(AVAILABLE_MODELS)


@refactoring_bp.route('/smells', methods=['GET'])
def get_smells():
    """Get available test smell types."""
    return jsonify({"smells": list(SMELL_DEFINITIONS.keys())})


@refactoring_bp.route('/health', methods=['GET'])
def health_check():
    """Check health status of refactoring service."""
    ollama_available = ensure_ollama()
    return jsonify({
        "status": "healthy",
        "ollama_available": ollama_available,
        "huggingface_configured": bool(HUGGINGFACE_API_KEY)
    })


@refactoring_bp.route('/refactor', methods=['POST'])
def refactor_code():
    """Refactor test code to remove test smells.
    
    Request body:
        {
            "code": str,           # Test code to refactor
            "smell_name": str,     # Name of the test smell
            "model_type": str,     # "ollama" or "huggingface"
            "model_name": str,     # Model identifier
            "agent_mode": str,     # "single" or "multi"
            "temperature": float   # LLM temperature (default 0.6)
        }
    
    Response:
        {
            "success": bool,
            "refactored_code": str,
            "detection_results": list,  # Only for multi-agent mode
            "error": str                # If any error occurred
        }
    """
    try:
        data = request.json
        code = data.get("code")
        smell_name = data.get("smell_name")
        model_type = data.get("model_type", "ollama")
        model_name = data.get("model_name", "llama3.2")
        agent_mode = data.get("agent_mode", "single")
        temperature = data.get("temperature", 0.6)
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        if smell_name not in SMELL_DEFINITIONS:
            return jsonify({"error": f"Unknown smell: {smell_name}"}), 400
        
        smell_def = SMELL_DEFINITIONS[smell_name]
        
        # Get LLM client
        client, model_name = get_llm(model_type, model_name, temperature)
        
        print(f"[API] Processing request with {agent_mode} agent mode")
        print(f"[API] Model: {model_name}, Smell: {smell_name}")
        
        if agent_mode == "single":
            # Single agent mode
            result = refactor_single_agent(
                client=client,
                model_name=model_name,
                code=code,
                smell_name=smell_name,
                smell_definition=smell_def,
                temperature=temperature
            )
            
            return jsonify({
                "success": result["success"],
                "refactored_code": result["refactored_code"],
                "detection_results": None,
                "error": result.get("error")
            })
        
        else:
            # Multi-agent mode
            result = refactor_multi_agent(
                client=client,
                model_name=model_name,
                code=code,
                smell_name=smell_name,
                smell_definition=smell_def,
                temperature=temperature,
                max_iters=3
            )
            
            return jsonify({
                "success": result["success"],
                "refactored_code": result["refactored_code"],
                "detection_results": result.get("detection_results"),
                "error": result.get("error")
            })
    
    except Exception as e:
        import traceback
        print(f"[API] Error occurred: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
