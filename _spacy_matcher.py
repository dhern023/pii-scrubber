"""
Functions to perform spacy matching, tagging, and replacement
"""
def construct_dict_match(instance_spacy, doc, match_id, start, end):
    dict_match = {}
    dict_match['key'] = instance_spacy.vocab.strings[match_id]  # Get string representation
    dict_match['text'] = doc[start:end].text  # The matched span
    dict_match['match_id'] = match_id

    return dict_match

def collect_matches(instance_spacy, doc, instance_matcher):
    """
    Works best on list of lists
    """
    list_tuple_matches = instance_matcher(doc)
    list_dict_matches = []
    for match_id, start, end in list_tuple_matches:
        dict_match = construct_dict_match(instance_spacy, doc, match_id, start, end)
        list_dict_matches.append(dict_match)

    return list_dict_matches

def replace_matches_in_doc(doc, list_dict_matches):
    """
    TODO: Replacing like this without walking an index is highly subject to error
    """
    string_p = doc.text
    for dict_match in list_dict_matches:
        string_p = string_p.replace(
            dict_match['text'], 
            f"[{dict_match['key']}]"
            )

    return string_p

def matcher_append_dict_patterns(instance_matcher, dict_patterns):
    """
    dict_patterns = { "label" : list_list_dict_pattern }
    """
    for key, value in dict_patterns.items():
        instance_matcher.add(key, value)
    
    assert instance_matcher.validate
    return instance_matcher