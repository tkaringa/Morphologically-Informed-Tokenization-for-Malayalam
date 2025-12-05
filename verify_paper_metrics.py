
import json
import os
import re
from tokenizers import Tokenizer
import sentencepiece as spm
import numpy as np

def calculate_metrics():
    print("Starting metrics verification...")
    
    # Load corpus sample
    corpus_path = "malayalam_raw_corpus.txt"
    sample_sentences = []
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 10000: break
                if line.strip():
                    sample_sentences.append(line.strip())
    except Exception as e:
        print(f"Error reading corpus: {e}")
        return

    print(f"Loaded {len(sample_sentences)} sample sentences.")
    
    # Count total tokens
    total_word_tokens = sum(len(s.split()) for s in sample_sentences)
    print(f"Total word tokens in sample: {total_word_tokens}")

    # Define tokenizer models
    models = [
        {"name": "BPE 8k", "path": "trained_tokenizers/bpe_raw_8000.json", "type": "bpe", "vocab": 8000},
        {"name": "Hybrid 8k", "path": "trained_tokenizers/bpe_morphological_8000.json", "type": "bpe", "vocab": 8000},
        {"name": "BPE 16k", "path": "trained_tokenizers/bpe_raw_16000.json", "type": "bpe", "vocab": 16000},
        {"name": "Hybrid 16k", "path": "trained_tokenizers/bpe_morphological_16000.json", "type": "bpe", "vocab": 16000},
        {"name": "BPE 32k", "path": "trained_tokenizers/bpe_raw_32000.json", "type": "bpe", "vocab": 32000},
        {"name": "Hybrid 32k", "path": "trained_tokenizers/bpe_morphological_32000.json", "type": "bpe", "vocab": 32000},
    ]

    results = {}

    for model in models:
        print(f"Evaluating {model['name']}...")
        fertility_scores = []
        oov_count = 0
        total_subwords = 0
        
        if not os.path.exists(model['path']):
            print(f"Model not found: {model['path']}")
            continue

        try:
            tokenizer = Tokenizer.from_file(model['path'])
            
            for sentence in sample_sentences:
                # Pre-tokenize for fertility
                words = sentence.split()
                for word in words:
                    encoded = tokenizer.encode(word)
                    tokens = encoded.tokens
                    ids = encoded.ids
                    
                    # Calculate fertility score
                    fertility_scores.append(len(tokens))
                    total_subwords += len(tokens)
                    
                    # Check for unknown tokens
                    # Detect UNK tokens
                    if '[UNK]' in tokens:
                        oov_count += 1
            
            avg_fertility = np.mean(fertility_scores)
            oov_rate = (oov_count / len(fertility_scores)) * 100
            # Calculate coverage percentage
            coverage = 100 - oov_rate
            
            results[model['name']] = {
                "fertility": avg_fertility,
                "oov_rate": oov_rate,
                "coverage": coverage
            }
            
        except Exception as e:
            print(f"Error evaluating {model['name']}: {e}")

    print("\n--- Tokenization Metrics Results ---")
    print(json.dumps(results, indent=2))

    # Analyze morphological statistics
    # Infer morpheme counts
    # Parse space-separated tokens
    print("\nAnalyzing Morphological Statistics...")
    morph_data_path = "enhanced_hybrid_training_data.txt"
    
    morpheme_counts = {}
    total_segmented_tokens_count = 0
    total_morphemes_count = 0
    
    # Read data subset
    # Limit to 100k lines
    try:
        with open(morph_data_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 100000: break 
                tokens = line.strip().split()
                for token in tokens:
                    # Process hybrid tokens
                    # Handle pre-segmented words
                    # Identify morpheme boundaries
                    # Read processor output
                    # Assume BPE-ready format
                    # Example segmentation
                    
                    morpheme_counts[token] = morpheme_counts.get(token, 0) + 1
                    total_morphemes_count += 1
                
                # Estimate original counts
                # Count unique types
    except Exception as e:
        print(f"Error reading morph data: {e}")

    print(f"Analyzed {i} lines of morphological data.")
    print(f"Total Morphemes Counted: {total_morphemes_count}")
    print(f"Unique Morpheme Types: {len(morpheme_counts)}")
    
    # Estimate morpheme average
    # Reference corpus stats
    # Assume segmented content
    # Check segmentation extent
    # Verify hybrid format
    
    # Compare token counts
    raw_tokens_per_line = total_word_tokens / len(sample_sentences)
    print(f"Avg Raw Tokens per Line: {raw_tokens_per_line}")
    
    # Read hybrid tokens
    hybrid_tokens_count = 0
    hybrid_lines_count = 0
    with open(morph_data_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 10000: break
            hybrid_tokens_count += len(line.split())
            hybrid_lines_count += 1
            
    hybrid_tokens_per_line = hybrid_tokens_count / hybrid_lines_count
    print(f"Avg Hybrid Tokens per Line: {hybrid_tokens_per_line}")
    
    estimated_morphemes_per_word = hybrid_tokens_per_line / raw_tokens_per_line
    print(f"Estimated Morphemes per Word (Global Fertility): {estimated_morphemes_per_word}")

if __name__ == "__main__":
    calculate_metrics()
