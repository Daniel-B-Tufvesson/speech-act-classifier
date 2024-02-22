
from typing import TextIO

act_names = {
    1: 'inform',
    2: 'question',
    3: 'directive',
    4: 'commissive'
}

def reformat_daily_dialog(dialogues_file, acts_file, target_file):
    """
    Reformat the daily dialog data to a single file.
    """

    print('Formatting dialogs')

    dialogues_source = open(dialogues_file)
    acts_source = open(acts_file)
    target_source = open(target_file, mode='wt')

    try:
        reformat_dd(dialogues_source, acts_source, target_source)
    finally:
        dialogues_source.close()
        acts_source.close()
        target_source.close()
    
    print ('Formatting complete!')


def reformat_dd(dialogues: TextIO, acts: TextIO, target: TextIO):
    """
    Reformat the daily dialog data to a single output.
    """
    line = 0
    for dialog_line, acts_line in zip(dialogues, acts):
        line += 1

        try:
            utterances = dialog_line.strip().split('__eou__')[0:-1]
            individual_acts = acts_line.strip().split(' ')
            parsed_utterances, parsed_acts = parse_dialog(utterances, individual_acts)

            for utterance, act in zip(parsed_utterances, parsed_acts):
                target.write(utterance)
                target.write('\n')
                target.write(act)
                target.write('\n\n')
        except Exception as e:
            print(f'Error occurred while parsing line {line}. Error: {e}')


def parse_dialog(utterances: list[str], acts: list[str]) -> tuple[list[str], list[str]]:
    """
    Parse a dialog given by its seqeuence of utterances and acts.
    """

    assert len(utterances) == len(acts), f'length of utterances and acts to not match {utterances}, {acts}'

    parsed_utterances = []
    parsed_acts = []
    for utterance, act in zip(utterances, acts):
        utterance = utterance.strip()
        act = int(act.strip())
        act = act_names[act]

        parsed_utterances.append(utterance)
        parsed_acts.append(act)
    
    return parsed_utterances, parsed_acts


if __name__ == '__main__':
    reformat_daily_dialog('dailydialog/ijcnlp_dailydialog/validation/dialogues_validation.txt', 
                          'dailydialog/ijcnlp_dailydialog/validation/dialogues_act_validation.txt',
                          'dailydialog/formatted data/dd_val.txt')