# Release Checklist

Use this checklist before tagging a release.

- [ ] Run `pip install -r requirements.txt` in a fresh environment.
- [ ] Re-generate hybrid corpus on a small sample to sanity-check pipeline.
- [ ] Re-train tokenizers (8k/16k/32k) and update `trained_tokenizers/training_summary.json`.
- [ ] Re-run analyses to produce tables and verify metrics match the paper.
- [ ] Build LaTeX with XeLaTeX/LuaLaTeX; ensure ACL style files are available.
- [ ] Update `CITATION.cff` version and `preferred-citation` if arXiv DOI becomes available.
- [ ] Confirm that large corpora are excluded by `.gitignore`.
- [ ] Push artifacts that are small and necessary (configs, small samples), not full datasets.
