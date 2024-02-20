"""

"""

from korp_to_connlu import Korp_CoNNLU_Converter
import file_inspector as fi
import connlu_cleaner as cl
import dep_parse_tagging as dep
import speech_act_classifier as sac

DIR_RAW_DATA = 'raw data'
DIR_NO_DEPS = 'processed data no-deps'
DIR_PROCESSED = 'processed data'
DIR_DATA_TO_ANNOTATE = 'data to annotate'

def process(corpus_name: str, genre: str, read_tail=False):

    # Print first lines from xml file.
    source_file = f'{DIR_RAW_DATA}/{corpus_name}.xml.bz2'
    fi.read_n_first_lines(source_file, 30)

    # Parse from xml to CoNNL-U.
    target_file = f'{DIR_NO_DEPS}/{corpus_name}-100k.connlu.bz2'
    print(f'Parsing xml "{source_file}" to CoNNL-U "{target_file}"')
    Korp_CoNNLU_Converter(genre=genre, read_tail=read_tail).xmlbz2_to_connlubz2(source_file, target_file, 100000)
    fi.read_n_first_lines(target_file, 30)

    # Clean up data
    source_file = target_file
    target_file = f'{DIR_NO_DEPS}/{corpus_name}-100k-clean.connlu.bz2'
    print(f'Cleaning up "{source_file}" to "{target_file}"')
    cl.clean_up_bz2(source_file, target_file)
    fi.read_n_first_lines(target_file, 30)

    # Parse dependency relations.
    source_file = target_file
    target_file = f'{DIR_PROCESSED}/{corpus_name}-100k.connlu.bz2'
    print(f'Parsing dependency relations "{source_file}" to "{target_file}"')
    dep.tag_bz2(source_file, target_file)
    fi.read_n_first_lines(target_file, 30)



if __name__ == '__main__':
    process('bloggmix2017', sac.Genre.INTERNET_BLOG.value, read_tail=False)