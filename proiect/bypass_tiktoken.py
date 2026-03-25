"""
Monkey patch to completely bypass tiktoken in LiteLLM
This prevents any attempts to download tiktoken encodings
"""
import sys
from unittest.mock import MagicMock

# Create a fake encoding class that behaves like a real tiktoken encoding
class FakeEncoding:
    """Fake tiktoken encoding that returns dummy values"""
    
    def __init__(self, name="cl100k_base"):
        self.name = name
        self.max_token_value = 100000
    
    def encode(self, text, allowed_special=None, disallowed_special=None):
        """Return a dummy token list - estimate ~4 chars per token"""
        if isinstance(text, str):
            # Rough estimate: 1 token per 4 characters
            num_tokens = max(1, len(text) // 4)
            return list(range(num_tokens))
        return []
    
    def encode_ordinary(self, text):
        """Same as encode but without special tokens"""
        return self.encode(text)
    
    def decode(self, tokens):
        """Return empty string for decoding"""
        return ""
    
    def decode_bytes(self, tokens):
        """Return empty bytes for decoding"""
        return b""

# Create fake tiktoken module
fake_tiktoken = MagicMock()
fake_encoding = FakeEncoding()

# Mock the main functions
fake_tiktoken.get_encoding = MagicMock(return_value=fake_encoding)
fake_tiktoken.encoding_for_model = MagicMock(return_value=fake_encoding)
fake_tiktoken.list_encoding_names = MagicMock(return_value=["cl100k_base", "p50k_base"])

# Mock the registry module
fake_registry = MagicMock()
fake_registry.get_encoding = MagicMock(return_value=fake_encoding)
fake_registry.ENCODING_CONSTRUCTORS = {"cl100k_base": lambda: fake_encoding}

# Inject the fake modules BEFORE any imports
sys.modules['tiktoken'] = fake_tiktoken
sys.modules['tiktoken.core'] = MagicMock()
sys.modules['tiktoken.model'] = MagicMock()
sys.modules['tiktoken.registry'] = fake_registry
sys.modules['tiktoken_ext'] = MagicMock()
sys.modules['tiktoken_ext.openai_public'] = MagicMock()

print("✓ Tiktoken bypass installed - all tiktoken calls will be mocked")
