"""
Validation script to test Llama 3.2 integration
Run this to verify everything is set up correctly
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_status(check_name, passed, message=""):
    status = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} {check_name}")
    if message:
        print(f"  → {message}")
    return passed

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return True, result.stdout.strip()
    except FileNotFoundError:
        return False, "Ollama not found in PATH"
    except Exception as e:
        return False, str(e)

def check_ollama_running():
    """Check if Ollama server is running"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def check_llama_model():
    """Check if Llama 3.2 model is pulled"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            has_llama = 'llama3.2' in result.stdout.lower()
            return has_llama, result.stdout
        return False, "Failed to list models"
    except Exception as e:
        return False, str(e)

def check_hf_token():
    """Check if HuggingFace token is set"""
    token = os.getenv('HF_TOKEN')
    if token and len(token) > 10:
        return True, f"Token set (length: {len(token)})"
    return False, "HF_TOKEN not found in environment"

def check_files_exist():
    """Check if modified files exist"""
    files_to_check = [
        'backend/modules/test_generator/ai_generator.py',
        'backend/routes/test_generation.py',
        'backend/config/settings.py',
        'frontend/src/components/TestGenerator.jsx',
        'LLAMA_INTEGRATION.md',
        'QUICKSTART_LLAMA.md',
        '.env.example'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        exists = Path(file_path).exists()
        print_status(f"  {file_path}", exists)
        all_exist = all_exist and exists
    
    return all_exist, f"{'All' if all_exist else 'Some'} files present"

def check_code_modifications():
    """Check if key code modifications are present"""
    checks = []
    
    # Check ai_generator.py for MODELS dictionary
    try:
        with open('backend/modules/test_generator/ai_generator.py', 'r') as f:
            content = f.read()
            has_models_dict = 'MODELS = {' in content
            has_llama_config = '"llama-3.2"' in content
            checks.append(('MODELS dictionary', has_models_dict))
            checks.append(('Llama 3.2 config', has_llama_config))
    except Exception as e:
        checks.append(('ai_generator.py', False))
    
    # Check TestGenerator.jsx for model selector
    try:
        with open('frontend/src/components/TestGenerator.jsx', 'r') as f:
            content = f.read()
            has_ai_model_state = 'aiModel' in content
            has_model_selector = 'model-selector' in content
            checks.append(('aiModel state', has_ai_model_state))
            checks.append(('Model selector UI', has_model_selector))
    except Exception as e:
        checks.append(('TestGenerator.jsx', False))
    
    all_passed = all(passed for _, passed in checks)
    for name, passed in checks:
        print_status(f"  {name}", passed)
    
    return all_passed, f"Code modifications {'complete' if all_passed else 'incomplete'}"

def test_ollama_api():
    """Test if Ollama API is accessible"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            return True, "Ollama API responding"
        return False, f"API returned status {response.status_code}"
    except ImportError:
        return None, "requests library not installed (optional check)"
    except Exception as e:
        return False, f"API not accessible: {str(e)}"

def main():
    print_header("🔍 Llama 3.2 Integration Validation")
    
    all_checks = []
    
    # System Requirements
    print_header("📋 System Requirements")
    passed, msg = check_ollama_installed()
    all_checks.append(print_status("Ollama installed", passed, msg))
    
    passed, msg = check_ollama_running()
    all_checks.append(print_status("Ollama server running", passed, msg))
    
    passed, msg = check_llama_model()
    all_checks.append(print_status("Llama 3.2 model available", passed, msg))
    if not passed:
        print("  💡 Hint: Run 'ollama pull llama3.2' to download the model")
    
    # API Configuration
    print_header("⚙️  Configuration")
    passed, msg = check_hf_token()
    all_checks.append(print_status("HuggingFace token (for GPT-OSS)", passed, msg))
    if not passed:
        print("  💡 Hint: Set HF_TOKEN environment variable for GPT-OSS model")
        print("  ℹ️  Note: Not required for Llama 3.2 (local)")
    
    passed, msg = test_ollama_api()
    if passed is not None:
        all_checks.append(print_status("Ollama API accessible", passed, msg))
    
    # Code Integration
    print_header("📁 File Structure")
    passed, msg = check_files_exist()
    all_checks.append(print_status("Required files", passed, msg))
    
    print_header("💻 Code Modifications")
    passed, msg = check_code_modifications()
    all_checks.append(print_status("Code changes", passed, msg))
    
    # Summary
    print_header("📊 Validation Summary")
    total_checks = len(all_checks)
    passed_checks = sum(all_checks)
    
    print(f"\nPassed: {passed_checks}/{total_checks} checks")
    
    if passed_checks == total_checks:
        print("\n✅ All checks passed! Your Llama 3.2 integration is ready.")
        print("\nNext steps:")
        print("  1. Start backend: python backend/app_unified.py")
        print("  2. Start frontend: cd frontend && npm run dev")
        print("  3. Open browser: http://localhost:5173")
        print("  4. Select AI mode and choose 'Llama 3.2 (Local)'")
    elif passed_checks >= total_checks * 0.7:
        print("\n⚠️  Most checks passed, but some issues need attention.")
        print("   Review the failures above and consult LLAMA_INTEGRATION.md")
    else:
        print("\n❌ Several checks failed. Please review the issues above.")
        print("   See QUICKSTART_LLAMA.md for setup instructions")
    
    print_header("📚 Documentation")
    docs = [
        ('Quick Start Guide', 'QUICKSTART_LLAMA.md'),
        ('Full Integration Guide', 'LLAMA_INTEGRATION.md'),
        ('Architecture Details', 'ARCHITECTURE_AI_MODELS.md'),
        ('Integration Summary', 'INTEGRATION_SUMMARY.md')
    ]
    for name, path in docs:
        exists = Path(path).exists()
        print_status(f"  {name}", exists, path)
    
    print("\n" + "=" * 70 + "\n")
    
    return 0 if passed_checks == total_checks else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
