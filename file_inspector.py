"""
A simple script for inspecting bz2 compressed corpus files.
"""

import bz2

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
    incremental_read('processed data/familjeliv-expert.connlu.bz2')
    pass