#!/bin/python3
import subprocess
import sys
from transformers import logging

logging.set_verbosity_error()

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
    parser.add_argument("--copy", action="store_true", help="Copy the generated code to clipboard.")
    parser.add_argument("prompt", nargs=argparse.REMAINDER, help="The prompt to generate code for.")
    args = parser.parse_args()

    if not args.prompt:
        print("Error: A prompt is required.")
        return
    prompt_text = " ".join(args.prompt)
    codegen = CodeGenerator()
    generated_code = codegen.generate_code(prompt_text)
    print(generated_code)
    if args.copy:
        import pyperclip
        pyperclip.copy(generated_code)
        print("\nGenerated code has been copied to clipboard.")

if __name__ == "__main__":
    main()
