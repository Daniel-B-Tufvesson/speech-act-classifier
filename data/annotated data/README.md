# `annotated data`
This directory contains the manually annotated data.

## Test Annotations
To create the annotation guidelines, I did some initial test annotations. This is commonly referred to as the MAMA subcycle in the MATTER development cycle. I annotated a subsample of sentences to find which sentences were problemamtic for the guidelines. These annotated sentences can be found in the `test annotations 1` directory. The guidelines were then adjusted to accomodate these sentences. I then annotated the subsample again, and these can be found in `test annotations 2`.

Cohen's kappa between these annotation samples is 0.835. I computed this with the `compute_cohens_kappa_dir` function in `annotate.py`.