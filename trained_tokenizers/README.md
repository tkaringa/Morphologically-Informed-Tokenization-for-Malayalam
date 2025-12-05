# Trained Malayalam Tokenizers

This directory contains tokenizer models trained on Malayalam text.

## Model Types

1.  **Raw Models (`*_raw_*`)**: Trained on the raw `malayalam_raw_corpus.txt`. These models tend to keep words whole if they are frequent.
2.  **Morphological Models (`*_morphological_*`)**: Trained on `enhanced_hybrid_training_data.txt`, which was pre-segmented using a morphological analyzer (`mlmorph`). These models are better at splitting agglutinated words into stems and suffixes.

## Architectures

*   **BPE (Byte-Pair Encoding)**: Trained using HuggingFace Tokenizers.
*   **SentencePiece (Unigram)**: Trained using Google's SentencePiece.

## Vocabulary Sizes

Models are available in 8000, 16000, and 32000 vocabulary sizes.

## Usage Example (Python)

```python
from tokenizers import Tokenizer
import sentencepiece as spm

# Load BPE
tokenizer = Tokenizer.from_file("trained_tokenizers/bpe_morphological_16000.json")
encoded = tokenizer.encode("മലയാളം")

# Load SentencePiece
sp = spm.SentencePieceProcessor(model_file="trained_tokenizers/sp_morphological_16000.model")
tokens = sp.encode("മലയാളം", out_type=str)
```
