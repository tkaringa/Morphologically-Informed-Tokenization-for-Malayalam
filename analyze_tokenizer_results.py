
import sentencepiece as spm
from tokenizers import Tokenizer
import json
import os

def analyze_tokenizers():
    sample_text = "ഡിജിറ്റൽ ഇന്ത്യയുടെ ഭാഗമായി 75000 കോടി രൂപ നിക്ഷേപിക്കുമെന്ന് ഗൂഗിള്‍ കഴിഞ്ഞ ദിവസം പ്രഖ്യാപിച്ചിരുന്നു."
    
    print(f"Sample Text: {sample_text}\n")
    print("-" * 50)

    # Analyze BPE models
    print("Analyzing BPE Models (Vocab Size: 16000)")
    bpe_models = {
        "Raw": "trained_tokenizers/bpe_raw_16000.json",
        "Morphological": "trained_tokenizers/bpe_morphological_16000.json"
    }

    for name, path in bpe_models.items():
        if os.path.exists(path):
            try:
                tokenizer = Tokenizer.from_file(path)
                encoded = tokenizer.encode(sample_text)
                print(f"\n{name} BPE Model:")
                print(f"Tokens: {encoded.tokens}")
                print(f"Count: {len(encoded.tokens)}")
            except Exception as e:
                print(f"Error loading {name} BPE: {e}")
        else:
            print(f"File not found: {path}")

    print("-" * 50)

    # Analyze SentencePiece models
    print("Analyzing SentencePiece Models (Vocab Size: 16000)")
    sp_models = {
        "Raw": "trained_tokenizers/sp_raw_16000.model",
        "Morphological": "trained_tokenizers/sp_morphological_16000.model"
    }

    for name, path in sp_models.items():
        if os.path.exists(path):
            try:
                sp = spm.SentencePieceProcessor(model_file=path)
                tokens = sp.encode(sample_text, out_type=str)
                print(f"\n{name} SentencePiece Model:")
                print(f"Tokens: {tokens}")
                print(f"Count: {len(tokens)}")
            except Exception as e:
                print(f"Error loading {name} SP: {e}")
        else:
            print(f"File not found: {path}")

if __name__ == "__main__":
    analyze_tokenizers()
