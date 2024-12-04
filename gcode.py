#!/bin/python3
import subprocess
import sys

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

try:
    import pyperclip
except ImportError:
    print("pyperclip not found, installing...")
    install_package("pyperclip")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
except ImportError:
    print("transformers not found, installing...")
    install_package("transformers")

try:
    from assistant import CodeGenerator
except ImportError:
    install_package("requests")
    import requests
    with open('assistant.py', 'w') as f:
        f.write(str(requests.get("https://raw.githubusercontent.com/guest3301/MACP/refs/heads/main/assistant.py").text))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate code from a prompt.")
    parser.add_argument("prompt", type=str, help="The prompt to generate code for.")
    parser.add_argument("--copy", action="store_true", help="Copy the generated code to clipboard.")
    args = parser.parse_args()
    codegen = CodeGenerator()
    generated_code = codegen.generate_code(args.prompt)
    print(generated_code)
    if args.copy:
        import pyperclip
        pyperclip.copy(generated_code)
        print("\nGenerated code has been copied to clipboard.")

if __name__ == "__main__":
    main()
