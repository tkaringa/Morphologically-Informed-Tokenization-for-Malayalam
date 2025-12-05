import os
import json
from collections import defaultdict
from pathlib import Path

# Import tokenizers library
try:
    from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers
    from tokenizers.processors import TemplateProcessing
    HAS_HF = True
except ImportError:
    HAS_HF = False
    print("warning: tokenizers not installed, skipping bpe training")

# Import SentencePiece library
try:
    import sentencepiece as spm
    HAS_SP = True
except ImportError:
    HAS_SP = False
    print("warning: sentencepiece not installed, skipping sp training")

# Define constants
VOCAB_SIZES = [8000, 16000, 32000]
OUT_DIR = "trained_tokenizers"

def prepare_raw_corpus(in_path, out_path):
    # Filter corpus quality
    print(f"preparing raw corpus: {in_path} -> {out_path}")
    
    count = 0
    kept = 0
    
    with open(in_path, 'r', encoding='utf-8') as f_in, \
         open(out_path, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            line = line.strip()
            count += 1
            
            # Perform basic checks
            if not line or len(line) < 10:
                continue
                
            # Check Malayalam content
            mal_chars = sum(1 for c in line if '\u0D00' <= c <= '\u0D7F')
            if mal_chars < len(line) * 0.4:
                continue
                
            # Check sentence length
            words = line.split()
            if len(words) < 3 or len(words) > 100:
                continue
                
            f_out.write(line + '\n')
            kept += 1
            
            if count % 50000 == 0:
                print(f"processed {count} lines, kept {kept}")

    print(f"done. retention: {kept/count*100:.1f}%")

def train_bpe(corpus_path, corpus_type, vocab_size):
    if not HAS_HF:
        return None
        
    print(f"training bpe-{vocab_size} on {corpus_type}...")
    
    try:
        # Initialize tokenizer
        tok = Tokenizer(models.BPE(unk_token="[UNK]"))
        
        tok.normalizer = normalizers.Sequence([
            normalizers.NFD(),
            normalizers.Lowercase(),
            normalizers.StripAccents()
        ])
        
        tok.pre_tokenizer = pre_tokenizers.Sequence([
            pre_tokenizers.WhitespaceSplit(),
            pre_tokenizers.Punctuation()
        ])
        
        trainer = trainers.BpeTrainer(
            vocab_size=vocab_size,
            min_frequency=2,
            special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
            show_progress=True
        )
        
        tok.train([corpus_path], trainer)
        
        # Configure post-processing
        tok.post_processor = TemplateProcessing(
            single="[CLS] $A [SEP]",
            pair="[CLS] $A [SEP] $B:1 [SEP]:1",
            special_tokens=[("[CLS]", 1), ("[SEP]", 2)]
        )
        
        # Save tokenizer model
        out_path = os.path.join(OUT_DIR, f"bpe_{corpus_type}_{vocab_size}.json")
        tok.save(out_path)
        print(f"saved to {out_path}")
        return out_path
        
    except Exception as e:
        print(f"error training bpe: {e}")
        return None

def train_sp(corpus_path, corpus_type, vocab_size):
    if not HAS_SP:
        return None
        
    print(f"training sp-{vocab_size} on {corpus_type}...")
    
    prefix = os.path.join(OUT_DIR, f"sp_{corpus_type}_{vocab_size}")
    
    try:
        spm.SentencePieceTrainer.train(
            input=corpus_path,
            model_prefix=prefix,
            vocab_size=vocab_size,
            model_type='bpe',
            character_coverage=0.9995,
            normalization_rule_name='nmt_nfkc_cf',
            split_by_whitespace=True
        )
        print(f"saved to {prefix}.model")
        return f"{prefix}.model"
        
    except Exception as e:
        print(f"error training sp: {e}")
        return None

if __name__ == "__main__":
    # Create output directory
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # Prepare training data
    raw_in = "malayalam_raw_corpus.txt"
    morph_in = "enhanced_hybrid_training_data.txt"
    
    files = {}
    
    # Process raw corpus
    if os.path.exists(raw_in):
        raw_out = os.path.join(OUT_DIR, "raw_training_corpus.txt")
        prepare_raw_corpus(raw_in, raw_out)
        files['raw'] = raw_out
    else:
        print(f"warning: {raw_in} not found")
        
    # Process morphological corpus
    if os.path.exists(morph_in):
        # Copy processed corpus
        morph_out = os.path.join(OUT_DIR, "morphological_training_corpus.txt")
        with open(morph_in, 'r', encoding='utf-8') as fin, \
             open(morph_out, 'w', encoding='utf-8') as fout:
            fout.write(fin.read())
        files['morphological'] = morph_out
        print(f"prepared morphological corpus: {morph_out}")
    else:
        print(f"warning: {morph_in} not found")
    
    # Train tokenizer models
    results = defaultdict(list)
    
    for c_type, c_path in files.items():
        for v_size in VOCAB_SIZES:
            # Train BPE model
            if path := train_bpe(c_path, c_type, v_size):
                results['bpe'].append(path)
                
            # Train SentencePiece model
            if path := train_sp(c_path, c_type, v_size):
                results['sentencepiece'].append(path)
    
    # Save training summary
    summary = {
        'models': dict(results),
        'vocab_sizes': VOCAB_SIZES
    }
    
    with open(os.path.join(OUT_DIR, "training_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
        
    print("done. summary saved.")
