"""
Script that prepends the string "# " to each non-empty line annotated
sentence files. 

So this: 

sent_id = 1300467
text = jag kanske inte tillför nåt nytt.
speech_act = assertion

becomes this:

# sent_id = 1300467
# text = jag kanske inte tillför nåt nytt.
# speech_act = assertion

"""

from context import speechact
import speechact.annotate as annotate
import os

if __name__ == '__main__':
    directory = 'data/annotated data/test annotations'
    file_names = annotate.annotation_files_in_dir(directory)

    for file_name in file_names:
        print(f'Prepending # to "{file_name}"')

        tmp_file = f'{directory}/tmp_corp.txt'

        with open(file_name, mode='rt') as source, open(tmp_file, mode='wt') as target:
            for line in source:
                if line.strip() == '':
                    target.write(line)
                elif not line.startswith('#'): 
                    line = f'# {line}'
                    target.write(line)

        os.replace(tmp_file, file_name)

