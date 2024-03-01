# `reindexed data`

This directory contains the same files as `processed data no-deps clean ` directory, except that each sentence has been reassigned a new `sent_id`. This ID is an autoincremented integer starting from 1, and spans over all the corpora in the directory. The ID is thus unique across the corpora, and not just within each corpus. Each sentence also has a `x_sent_id` which is its original ID from its corpus.

The `data files.txt` file lists all the files that should be included in the thesis, i.e. used for training and evaluation.