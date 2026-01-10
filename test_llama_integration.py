"""
Example script to test Llama 3.2 integration with PyTestGenie AI Test Generator
Run this after setting up Llama 3.2 with Ollama
"""

# Sample Python code to generate tests for
sample_code = """
def calculate_discount(price, discount_percent):
    '''Calculate the final price after applying discount.'''
    if price < 0 or discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid price or discount")
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount

def is_palindrome(text):
    '''Check if a string is a palindrome.'''
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]
"""

print("=" * 60)
print("Llama 3.2 Integration Test")
print("=" * 60)
print("\nSample code to test:\n")
print(sample_code)
print("\n" + "=" * 60)
print("\nTo test the integration:")
print("\n1. Start your backend server:")
print("   python backend/app_unified.py")
print("\n2. Start your frontend:")
print("   cd frontend && npm run dev")
print("\n3. In the web UI:")
print("   - Select 'AI (OpenAI/HuggingFace)' option")
print("   - Choose 'Llama 3.2 (Local)' from AI Model dropdown")
print("   - Paste the sample code above")
print("   - Click 'Generate Tests'")
print("\n4. Or test via API:")
print("   curl -X POST http://localhost:5000/api/test-generator/generate-tests/ai \\")
print("     -H 'Content-Type: application/json' \\")
print("     -d '{\"code\": \"<your_code>\", \"model\": \"llama-3.2\"}'")
print("\n" + "=" * 60)
print("\nVerify Ollama is running:")
print("   ollama list")
print("   ollama run llama3.2 'Hello'")
print("\n" + "=" * 60)
