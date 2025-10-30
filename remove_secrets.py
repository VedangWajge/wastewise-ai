"""
Script to remove API keys and secrets from documentation files
Run this before committing to git
"""
import os
import re

# Patterns to find and replace
PATTERNS = {
    # Google Gemini API Keys
    r'AIzaSy[A-Za-z0-9_-]{33}': 'AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',

    # OpenAI API Keys
    r'sk-proj-[A-Za-z0-9_-]{100,}': 'sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    r'sk-[A-Za-z0-9]{48}': 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',

    # Hugging Face tokens
    r'hf_[A-Za-z0-9]{30,}': 'hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',

    # Razorpay Keys
    r'rzp_test_[A-Za-z0-9]{14}': 'rzp_test_XXXXXXXXXXXXX',
    r'rzp_live_[A-Za-z0-9]{14}': 'rzp_live_XXXXXXXXXXXXX',

    # Razorpay Key Secrets (longer)
    r'[A-Za-z0-9]{24}(?=\s|$)': '[REDACTED_SECRET]',
}

# Files to process (documentation only, not code)
DOCUMENTATION_EXTENSIONS = ['.md', '.txt', '.rst']

def sanitize_file(filepath):
    """Remove secrets from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = False

        for pattern, replacement in PATTERNS.items():
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                changes_made = True
                matches = len(re.findall(pattern, content))
                print(f"  [OK] Replaced {matches} instance(s) of {pattern[:20]}...")
            content = new_content

        if changes_made:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def scan_directory(directory):
    """Scan directory for files to sanitize"""
    sanitized_files = []

    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        skip_dirs = {'node_modules', 'venv', 'env', '__pycache__', '.git', 'build', 'dist'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            # Only process documentation files
            if any(file.endswith(ext) for ext in DOCUMENTATION_EXTENSIONS):
                filepath = os.path.join(root, file)
                print(f"Checking: {filepath}")

                if sanitize_file(filepath):
                    sanitized_files.append(filepath)

    return sanitized_files

def main():
    print("=" * 60)
    print("SECRET REMOVAL TOOL")
    print("=" * 60)
    print("\nThis script will remove API keys and secrets from documentation files.")
    print("It will NOT modify code files or .env files.\n")

    current_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"Scanning directory: {current_dir}\n")

    sanitized = scan_directory(current_dir)

    print("\n" + "=" * 60)
    if sanitized:
        print(f"[SUCCESS] Sanitized {len(sanitized)} file(s):")
        for filepath in sanitized:
            print(f"  - {os.path.relpath(filepath, current_dir)}")
    else:
        print("[SUCCESS] No secrets found in documentation files")
    print("=" * 60)

    print("\nIMPORTANT:")
    print("1. Review the changes made to ensure correctness")
    print("2. Never commit .env files to git")
    print("3. Use .env.example with placeholder values instead")
    print("\nYou can now safely commit these files to git.")

if __name__ == "__main__":
    main()
