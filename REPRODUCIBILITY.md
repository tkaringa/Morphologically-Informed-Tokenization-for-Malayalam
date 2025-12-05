# Reproducibility Guide

This document outlines how to reproduce the key results in the paper.

## Environment
- Python 3.10+
- Install dependencies:
  - See `requirements.txt`

## Data
- Primary corpus: IndicCorp v2 (Malayalam). Due to licensing, raw data is not redistributed.
- Use the script `download_corpus.py` to fetch the corpus, or follow the dataset’s official instructions.

## Pipeline Overview
1. Prepare hybrid corpus with morphological pre-segmentation (`prepare_hybrid_corpus.py` or `prepare_hybrid_corpus_v2.py`).
2. Train baseline BPE tokenizers (see `baseline_tokenizer_training.py`).
3. Train hybrid tokenizers with pre-segmented data (see `enhanced_corpus_processor.py`).
4. Compute metrics and tables (coverage, fertility, OOV) with analysis scripts (e.g., `final_analysis.py` / `final_analysis_clean.py`, `analyze_corpus_stats.py`).
5. Validate boundaries vs mlmorph (see `debug_morphology.py` and `morphological_evaluation_system.py`).

## Seeds and Configs
- Default random seeds: 42, 123, 2024 (averaged where reported).
- SentencePiece (BPE) configs: vocab sizes = {8k, 16k, 32k}; character coverage = 0.9995; default normalization; no pretokenization.
- Configuration summaries are stored (or will be stored) in `trained_tokenizers/training_summary.json`.

## Expected Artifacts
- `trained_tokenizers/` will contain `.model`/`.vocab` files for SP tokenizers and `.json` for HuggingFace tokenizers.
- Tables and figures are exported to `academic_paper_output/`.

## Notes
- Malayalam script handling requires Unicode-safe processing; the LaTeX build uses XeLaTeX/LuaLaTeX.
- We do not redistribute IndicCorp v2; scripts provided will re-create the exact splits.
