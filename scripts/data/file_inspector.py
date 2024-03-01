"""
A simple script for inspecting bz2 compressed corpus files.
"""

import bz2

def read_n_first_lines(file_name: str, n_lines = 30):
    """
    Read the first N lines in the file.
    """
    with bz2.open(file_name, mode='rt') as source:
        print(f'Printing the first {n_lines} in "{file_name}" ---------------------')

        i = 0
        for line in source:
            print(line)
            i += 1

            if i == n_lines:
                break

        print(f'Printed the first {i}/{n_lines} in {file_name} ----------------------')


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
    #incremental_read('processed data/famtest.connlu.bz2')
    #incremental_read('raw data/suc3.xml.bz2')
    #incremental_read('processed data/suc3.connlu.bz2')
    #incremental_read('raw data/familjeliv-expert.xml.bz2')
    #incremental_read('processed data/familjeliv-expert.connlu.bz2')
    #incremental_read('processed data no-pos/attasidor-100k.connlu.bz2')
    #incremental_read('processed data/attasidor-99k.connlu.bz2')
    #incremental_read('raw data/gp2013.xml.bz2')
    #incremental_read('processed data no-deps/gp2013-100k.connlu.bz2')
    incremental_read('processed data/bloggmix2017-100k.connlu.bz2')
    pass