"""
Uses SpaCy to construct tags to match
"""

import _clean
import _import
import _dates
import _spacy_matcher

import argparse
import pathlib
import tqdm
import spacy
import spacy.matcher

parser = argparse.ArgumentParser(description="Scrub PII from text")
parser.add_argument('--generic', action='store_true', help='Scrub generic items')
parser.add_argument('--nouns', action='store_true', help='Scrub nouns')
parser.add_argument('--client', action='store_true', help='Scrub-specific rules for clients')
args = parser.parse_args()


if __name__ == "__main__":

    nlp = spacy.load('en_core_web_sm')
    matcher = spacy.matcher.Matcher(nlp.vocab)
    dict_patterns = _import.read_json_to_dict('patterns.json')
    if args.generic:
        matcher = _spacy_matcher.matcher_append_dict_patterns(
            matcher, dict_patterns['generic'])

    if args.nouns:
        matcher = _spacy_matcher.matcher_append_dict_patterns(
            matcher, dict_patterns['nouns'])

    if args.client:
        matcher = _spacy_matcher.matcher_append_dict_patterns(
            matcher, dict_patterns['client'])

    path_files = pathlib.Path.cwd() / 'data'
    list_files = list(path_files.rglob("*"))

    corpus = []
    for file in list_files:
        lines = _import.lazy_load_txt(file)
        text = " ".join(lines)
        corpus.append(text)

    list_tuple_cleaned_text = []
    for text in tqdm.tqdm(corpus, desc='Cleaning dates'):
        try:
            cleaned = _dates.clean_dates(text)
        except:
            index_file = corpus.index(text)
            print(list_files[index_file])
            cleaned = text
        list_tuple_cleaned_text.append(cleaned)

    # Run spacy matching
    list_docs = [nlp(text_p[0]) for text_p in tqdm.tqdm(list_tuple_cleaned_text)]
    dict_doc_matches = {}
    for doc in tqdm.tqdm(list_docs, desc='Collecting matches'):
        dict_doc_matches[doc] = _spacy_matcher.collect_matches(nlp, doc, matcher)

    # Cleanup
    list_text_p = []
    for doc, list_dict_matches in tqdm.tqdm(dict_doc_matches.items(), desc='Cleaning matches'):
        text_p = _spacy_matcher.replace_matches_in_doc(doc, list_dict_matches)
        list_text_p.append(text_p)

    # Export
    path_out = pathlib.Path.cwd() / 'out'
    path_out.mkdir(parents=True, exist_ok = True)
    for file, cleaned in zip(list_files, list_text_p):
        (path_out / file.stem).write_text(cleaned)
    

