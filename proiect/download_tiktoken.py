"""Script pentru pre-descărcarea encoding-urilor tiktoken"""
import tiktoken
import sys

try:
    print("Downloading tiktoken encodings...")
    # Descarcă toate encoding-urile posibile
    for enc_name in ['cl100k_base', 'p50k_base', 'r50k_base', 'p50k_edit', 'gpt2']:
        try:
            enc = tiktoken.get_encoding(enc_name)
            print(f"✓ Downloaded {enc_name}")
        except Exception as e:
            print(f"✗ Failed {enc_name}: {e}")
    print("Tiktoken encodings ready!")
except Exception as e:
    print(f"Warning: {e}")
    sys.exit(0)  # Nu eșuăm build-ul
