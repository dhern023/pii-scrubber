from csv import list_dialects
import _import
import _spacy_matcher

import pytest
import spacy
import spacy.matcher

cases_emails = (
    ("From: phillip.allen@enron.com To:", "From: [email] To:"),
    ("To: matthew.lenhart@enron.com, jay.reitmeyer@enron.com, matt.smith@enron.com ", "To: [email], [email], [email] "),
    # ("Jay Reitmeyer/HOU/ECT@ECT", "Jay [email]")
)

cases_client = (
    (" X-From: Phillip K Allen X-To:", "X-From: [email] X-To:"),
)

@pytest.fixture(scope='module')
def spacy_nlp():
    yield spacy.load('en_core_web_sm')

@pytest.fixture(scope='module')
def spacy_matcher(spacy_nlp):
    yield spacy.matcher.Matcher(spacy_nlp.vocab)

@pytest.fixture(scope='module')
def patterns():
    yield _import.read_json_to_dict('patterns.json')

@pytest.fixture(scope='module')
def generic(spacy_matcher, patterns):
    assert 'generic' in patterns
    assert isinstance(patterns['generic'], dict)
    yield _spacy_matcher.matcher_append_dict_patterns(spacy_matcher, patterns['generic'])

@pytest.fixture(scope='module')
def client(spacy_matcher, patterns):
    assert 'client' in patterns
    assert isinstance(patterns['client'], dict)
    yield _spacy_matcher.matcher_append_dict_patterns(spacy_matcher, patterns['client'])

def test_read_json_as_dict(patterns):
    assert isinstance(patterns, dict)

@pytest.mark.parametrize('string, expected', cases_emails)
def test_generic_emails(string, expected, spacy_nlp, generic):
    doc = spacy_nlp(string)
    list_dict_matches = _spacy_matcher.collect_matches(spacy_nlp, doc, generic)
    string_p = _spacy_matcher.replace_matches_in_doc(doc, list_dict_matches)
    assert string_p == expected

@pytest.mark.parametrize('string, expected', cases_client)
def test_generic_emails(string, expected, spacy_nlp, client):
    doc = spacy_nlp(string)
    print("doc", doc)
    list_dict_matches = _spacy_matcher.collect_matches(spacy_nlp, doc, client)
    print(list_dict_matches)
    string_p = _spacy_matcher.replace_matches_in_doc(doc, list_dict_matches)
    assert string_p == expected