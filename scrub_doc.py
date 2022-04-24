"""
Uses SpaCy to construct tags to match
"""

import _import
import _dates

import argparse
import pathlib
import tqdm
import spacy
from spacy.matcher import Matcher

parser = argparse.ArgumentParser(description="Scrub PII from text")
parser.add_argument('--generic', action='store_true', help='Scrub generic items')
parser.add_argument('--nouns', action='store_true', help='Scrub nouns')
parser.add_argument('--client', action='store_true', help='Scrub-specific rules for clients')
args = parser.parse_args()

def construct_dict_match(doc, match_id, start, end):
    dict_match = {}
    dict_match['key'] = nlp.vocab.strings[match_id]  # Get string representation
    dict_match['text'] = doc[start:end].text  # The matched span text
    dict_match['match_id'] = match_id

    return dict_match

def collect_matches(doc, instance_matcher):
    """
    Works best on list of lists
    """ 
    list_tuple_matches = instance_matcher(doc)
    list_dict_matches = []
    for match_id, start, end in list_tuple_matches:
        dict_match = construct_dict_match(doc, match_id, start, end)
        list_dict_matches.append(dict_match)

    return list_dict_matches

def replace_pii_in_doc(string, dict_match):
    """
    tuple_match = (match_id, doc_index_start, doc_index_end)
    """
    string_p = string.replace(dict_match['text'], '[{}]'.format(dict_match['key']))

    return string_p

def matcher_append_dict_patterns(instance_matcher, dict_patterns):
    """
    dict_patterns = { "label" : list_list_dict_pattern }
    """
    for key, value in dict_patterns.items():
        instance_matcher.add(key, value)
    
    assert instance_matcher.validate
    return instance_matcher

if __name__ == "__main__":

    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)
    dict_patterns = _import.read_json_to_dict('patterns.json')
    if args.generic:
        matcher = matcher_append_dict_patterns(
            matcher, dict_patterns['generic'])

    if args.nouns:
        matcher = matcher_append_dict_patterns(
            matcher, dict_patterns['nouns'])

    if args.client:
        matcher = matcher_append_dict_patterns(
            matcher, dict_patterns['client'])

    path_files = pathlib.Path.cwd() / 'data'
    list_files = list(path_files.rglob("*"))

    corpus = []
    for file in list_files:
        lines = _import.lazy_load_txt(file)
        text = " ".join(lines)
        corpus.append(text)

    list_tuple_cleaned_text = []
    for text in tqdm.tqdm(corpus):
        try:
            cleaned = _dates.clean_dates(text)
        except: # Horribly broken for now
            index_file = corpus.index(text)
            print(list_files[index_file])
            cleaned = text
        list_tuple_cleaned_text.append(cleaned)

    # Run spacy matching
    list_docs = [nlp(text_p[0]) for text_p in tqdm.tqdm(list_tuple_cleaned_text)]
    list_list_dict_matches = [collect_matches(doc, matcher) for doc in tqdm.tqdm(list_docs)]

    # Cleanup
    list_strings_p = []
    for index, doc in enumerate(list_docs):
        string_p = doc.text
        for dict_match in list_list_dict_matches[index]:
            string_p = replace_pii_in_doc(string_p, dict_match)
        list_strings_p.append(string_p)

    # Export
    path_out = pathlib.Path.cwd() / 'out'
    path_out.mkdir(parents=True, exist_ok = True)
    for file, cleaned in zip(list_files, list_strings_p):
        (path_out / file.stem).write_text(cleaned)
    

