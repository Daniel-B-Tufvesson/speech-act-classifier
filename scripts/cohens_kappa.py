"""
This script computes Cohen's kappa between two directories of annotated sentence corpora.
"""

# Example: python cohens_kappa.py 'data/annotated data/test annotations 1' 'data/annotated data/test annotations 2'
# Alternatively: python scripts/cohens_kappa.py 'data/annotated data/test annotations 1' 'data/annotated data/test annotations 2'

from context import speechact
import speechact.annotate as annotate
import sys

if __name__ == '__main__':
    
    # Check the number of arguments passed
    if len(sys.argv) != 3:
        print('Usage: python cohens_kappa.py <directory 1> <directory 2>')
        sys.exit(1)

    dir_1 = sys.argv[1]
    dir_2 = sys.argv[2]

    kappa = annotate.compute_cohens_kappa_dir(dir_1, dir_2)
    print(f"Cohen's kappa: {kappa}")

