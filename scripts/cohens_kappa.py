"""
This script computes Cohen's kappa between two directories of annotated sentences.
"""

from context import speechact
import speechact.annotate as annotate

if __name__ == '__main__':
    dir_1 = 'data/annotated data/test annotations 1'
    dir_2 = 'data/annotated data/test annotations 2'

    kappa = annotate.compute_cohens_kappa_dir(dir_1, dir_2)
    print(f"Cohen's kappa: {kappa}")
