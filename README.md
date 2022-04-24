# PII-Scrubber

Proof of concept NLP Scrubber

- Uses dateutil.parser to find dates
- Uses SpaCy to construct certain tags
- TODO: Will support nouns

# Setup

```
pip install -r requirements.txt
```

- Put a data folder at root with your text file(s)
- Add entries to patterns.json under "client" section as { key : list_list_dict }

NOTE: SpaCy patterns are lists of dicts, so any matcher will need a list of lists of dicts

# Running

```
py scrub_doc.py --generic --nouns[broken] --client[broken]
```
