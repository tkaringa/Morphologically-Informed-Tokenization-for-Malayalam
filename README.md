# Morphologically-Informed Tokenization for Malayalam

This repository contains code and paper artifacts for a hybrid tokenization approach that applies morphological pre-segmentation with mlmorph, followed by subword training (BPE/SentencePiece). It includes scripts to prepare a corpus, run the enhanced processor, train baselines, and build the ACL-style paper.

## Quickstart

Prerequisites:
- Python 3.10+
- Windows PowerShell (the examples below use PowerShell)

1) Create a small sample corpus (safe to commit size-wise):

```powershell
python .\create_sample_corpus.py
```

This writes `malayalam_raw_corpus.txt` (~a few MB) with morphologically diverse Malayalam sentences.

2) Run the enhanced morphological processor to produce the hybrid training data and a small results table:

```powershell
python .\enhanced_corpus_processor.py
```

Outputs:
- `enhanced_hybrid_training_data.txt` — pre-segmented corpus with `_SEP_` marking morpheme boundaries
- `enhanced_results_table.tex` — LaTeX table with core metrics (used in the paper)

3) Train baseline tokenizers for comparison (BPE + SentencePiece) using both raw and morphologically segmented corpora:

```powershell
python .\baseline_tokenizer_training.py
```

Outputs are saved under `trained_tokenizers/` (JSON models for BPE and `.model/.vocab` for SentencePiece), plus a consolidated `training_summary.json`.

4) Build the paper (optional):
- Paper sources live in `academic_paper_output/`.
- For review style (neutral/anonymized), use `malayalam_morphological_tokenization_acl_neutral.tex`.
- For camera-ready first-person style, use `malayalam_morphological_tokenization_acl_first_person.tex`.
- Ensure ACL style files are present (see that folder) and compile with your LaTeX engine. If XeLaTeX/LuaLaTeX is used, Malayalam fonts are handled in the preamble.

## Scripts
- `enhanced_corpus_processor.py` — runs the morphological segmentation pipeline end-to-end and writes `enhanced_hybrid_training_data.txt` plus a LaTeX results table.
- `baseline_tokenizer_training.py` — trains BPE and SentencePiece baselines on raw and morphologically segmented corpora; writes artifacts to `trained_tokenizers/`.
- `create_sample_corpus.py` — generates a compact Malayalam sample corpus suitable for demos and tests.
- `download_corpus.py` — downloads IndicCorp v2 Malayalam data (requires network access).

## Installation
Install dependencies into your environment:

```powershell
pip install -r .\requirements.txt
```

If you prefer a virtual environment, create one first (PowerShell):

```powershell
python -m venv .venv; . .\.venv\Scripts\Activate.ps1; pip install -r .\requirements.txt
```

## Notes and guidance
- Large corpora are not bundled. Use `create_sample_corpus.py` for a small demo, or `download_corpus.py` to obtain IndicCorp v2 Malayalam.
- The enhanced processor includes quality filtering and reports segmentation coverage and morpheme diversity.
- Training artifacts can be large; they are ignored by default via `.gitignore`, with a small `training_summary.json` retained for bookkeeping.
- Development artifacts are archived in `archive/` folder for historical context.

## Citation
If you use this code or paper, please cite the repository. See `CITATION.cff`.
