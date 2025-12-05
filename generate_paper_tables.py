
import json
import os
from tokenizers import Tokenizer
import sentencepiece as spm

def generate_latex_tables():
    # Define sample words
    sample_words = [
        "ഇന്ത്യയുടെ",      # India's
        "നിക്ഷേപിക്കുമെന്ന്", # Will invest
        "പ്രഖ്യാപിച്ചിരുന്നു", # Had announced
        "ഭാഗമായി"          # As part of
    ]
    
    # Load tokenizer models
    bpe_raw_path = "trained_tokenizers/bpe_raw_16000.json"
    bpe_morph_path = "trained_tokenizers/bpe_morphological_16000.json"
    
    if not os.path.exists(bpe_raw_path) or not os.path.exists(bpe_morph_path):
        print("Models not found. Skipping qualitative table.")
        return

    tokenizer_raw = Tokenizer.from_file(bpe_raw_path)
    tokenizer_morph = Tokenizer.from_file(bpe_morph_path)

    # Generate qualitative table
    latex_qual = []
    latex_qual.append("\\begin{table*}[h]")
    latex_qual.append("\\centering")
    latex_qual.append("\\caption{Qualitative Comparison of Tokenization Strategies (BPE 16k)}")
    latex_qual.append("\\begin{tabular}{l l l}")
    latex_qual.append("\\toprule")
    latex_qual.append("\\textbf{Word} & \\textbf{Raw Tokenization} & \\textbf{Morphological Tokenization} \\\\")
    latex_qual.append("\\midrule")

    for word in sample_words:
        raw_tokens = tokenizer_raw.encode(word).tokens
        morph_tokens = tokenizer_morph.encode(word).tokens
        
        # Format tokens
        raw_str = " + ".join([t.replace("##", "") for t in raw_tokens])
        morph_str = " + ".join([t.replace("##", "") for t in morph_tokens])
        
        latex_qual.append(f"\\mal{{{word}}} & \\mal{{{raw_str}}} & \\mal{{{morph_str}}} \\\\")

    latex_qual.append("\\bottomrule")
    latex_qual.append("\\end{tabular}")
    latex_qual.append("\\label{tab:qualitative-comparison}")
    latex_qual.append("\\end{table*}")

    with open("academic_paper_data/latex_tables.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(latex_qual))
    
    print("Generated qualitative table in academic_paper_data/latex_tables.tex")

    # Generate quantitative table
    # Need larger sample
    # Use sample text
    # Use available text
    sample_text = "ഡിജിറ്റൽ ഇന്ത്യയുടെ ഭാഗമായി 75000 കോടി രൂപ നിക്ഷേപിക്കുമെന്ന് ഗൂഗിള്‍ കഴിഞ്ഞ ദിവസം പ്രഖ്യാപിച്ചിരുന്നു."
    
    models = [
        ("Raw BPE 8k", "trained_tokenizers/bpe_raw_8000.json", "bpe"),
        ("Morph BPE 8k", "trained_tokenizers/bpe_morphological_8000.json", "bpe"),
        ("Raw BPE 16k", "trained_tokenizers/bpe_raw_16000.json", "bpe"),
        ("Morph BPE 16k", "trained_tokenizers/bpe_morphological_16000.json", "bpe"),
        ("Raw BPE 32k", "trained_tokenizers/bpe_raw_32000.json", "bpe"),
        ("Morph BPE 32k", "trained_tokenizers/bpe_morphological_32000.json", "bpe"),
    ]

    latex_quant = []
    latex_quant.append("\\begin{table}[h]")
    latex_quant.append("\\centering")
    latex_quant.append("\\caption{Tokenization Fertility (Tokens per Sentence) on Sample Text}")
    latex_quant.append("\\begin{tabular}{l c}")
    latex_quant.append("\\toprule")
    latex_quant.append("\\textbf{Model} & \\textbf{Token Count} \\\\")
    latex_quant.append("\\midrule")

    for name, path, mtype in models:
        if os.path.exists(path):
            if mtype == "bpe":
                tok = Tokenizer.from_file(path)
                count = len(tok.encode(sample_text).tokens)
                latex_quant.append(f"{name} & {count} \\\\")
    
    latex_quant.append("\\bottomrule")
    latex_quant.append("\\end{tabular}")
    latex_quant.append("\\label{tab:quantitative-stats}")
    latex_quant.append("\\end{table}")

    with open("academic_paper_data/latex_tables.tex", "a", encoding="utf-8") as f:
        f.write("\n\n")
        f.write("\n".join(latex_quant))

    print("Appended quantitative table to academic_paper_data/latex_tables.tex")

if __name__ == "__main__":
    generate_latex_tables()
