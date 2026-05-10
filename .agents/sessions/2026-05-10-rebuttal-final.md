# Session: Rebuttal Final Polish & Submission (2026-05-10)

## Summary
Completed final polish of ECCV 2026 OREO rebuttal (`rebuttal.tex` → `rebuttal.pdf`), addressing three reviewers (Nz3M, Ydh5, 1rPv). Copied final PDF to `OREO_rebuttal.pdf` for submission.

## Final Document State

### Layout
- **1-page** two-column rebuttal, ECCV format
- **Left column**: Opening paragraph → Reviewer Nz3M (Q1–Q4) → Reviewer Ydh5 (Q1, partial)
- **Right column**: Reviewer Ydh5 (Q1 cont., Q2–Q3) → Reviewer 1rPv (Q1–Q4)
- **Figure R1** (multi-view comparison): top-left, `[H]` placement
- **Figure R2** (editing trajectories w/ neg source guidance): top-right, `[t]` placement
- **Table R1** (Toy4K evaluation): right column below Figure R2, `[t]` placement
- Figure/table numbering uses `R` prefix via `\renewcommand{\thefigure}{R\arabic{figure}}`

### Key Content Decisions
- **Reviewer IDs**: Nz3M (#1), Ydh5 (#2), 1rPv (#3) — from review images
- **Human eval (Nz3M Q3)**: 41%/36%/23% (OREO/Photo3D/Trellis), evaluating "multi-view renderings' fidelity and consistency with the input image"
- **Computational overhead (Nz3M Q4)**: 81% sequential → 45% with async overlap, same hardware
- **Noise update ablation (1rPv Q2)**: Strengthens editing model prior alignment but may inherit color bias; confirmed by Table 3 + Table R1 (distributional similarity to GT renderings)
- **Table R1**: Includes OREO (w/o noise update) row with metrics 86.83/9.39/67.41/0.72, separated by `\midrule`
- **Dataset Q2 (Ydh5)**: "We will add these details in the next version and release this dataset."

### Compilation Notes
- Must run `pdflatex` **twice** for `hyperref` cross-references (R prefix in `\ref` links)
- `lineno` `[switch]` mode: line 074 misplacement fixed by adding `\vspace{-1mm}` above Table R1 to balance column heights
- Very tight on 1-page limit — any text additions require compensating cuts elsewhere

### Files
- `rebuttal.tex` — source (127 lines)
- `rebuttal.pdf` — compiled output
- `OREO_rebuttal.pdf` — submission copy
- `figures_rebuttal/mv_comparison_00250_04198_03360.png` — Figure R1
- `figures_rebuttal/comparison_grid.png` — Figure R2
- `rebuttal_preview.png` — last PNG preview for visual verification

### Known Quirks / Pitfalls
- Column height imbalance causes `lineno` line number misplacement (e.g., 074 jumping to left column bottom). Fix: adjust `\vspace` on Table R1.
- `\renewcommand{\thefigure}` only affects captions; in-text `\ref` needs second pdflatex pass for `hyperref` to pick up the R prefix.
- `\showreviewtagsfalse` hides reviewer tag annotations in the PDF; toggle to `\showreviewtagstrue` for internal review.
