"""
A simple script for inspecting bz2 compressed corpus files.

Usage: python view_bz2_file.py <bz2 text file>
"""
# Example: python scripts/view_bz2_file.py 'data/test-set.conllu.bz2'
import bz2
import sys

def incremental_read(file_name: str):
    """
    Stepwise read 100 lines of the file at a time.
    """
    with bz2.open(file_name, mode='rt') as source:
        print('printing 100 lines ------------------------------------')
        i = 0
        for line in source:
            print(line)
            i += 1

            if i == 100:
                i = 0
                input('press for next 100 lines-------------------------')
    
    print('full file has been printed.')


if __name__ == '__main__':

    # Check the number of arguments passed.
    if len(sys.argv) != 2:
        print('Usage: python view_bz2_file.py <bz2 text file>')
        sys.exit(1)

    file_name = sys.argv[1]
    incremental_read(file_name)
