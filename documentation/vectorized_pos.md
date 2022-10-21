## vectorized_pos(text)
This method will return a vectorized form of given `text`. Each scaler maps to a index derived from the dictionary used in the package.

```python
POS_type = 
    {
        "noun" : 1,
        "pronoun" : 2,
        "adjective" : 3,
        "verb" : 4,
        "adverb" : 5,
        "puncuation": 6
    }
```

```md
noun_response = [ POS_type, prefix_id, suffix_id]
```

```md
pronoun_response = [ POS_type, pronoun_id, pronoun_tag, number_tag, honorificity, case, proximity]
```

```md
adjective_response = [ POS_type, prefix_id, suffix_id]
```

```md
verb_response = [ POS_type, verb_id, tense_id, person_id, negation_id]
```

```md
adverb_response = [ POS_type, verb_id, tense_id, person_id, negation_id]
```

```md
puncuation_response = [ POS_type, prefix_id, suffix_id]
```

```md
  tense_map = 
    {   
        "sb": 0,
        "gb": 1,
        "pb": 2,
        "bo": 3,
        "so": 4,
        "no": 5,
        "go": 6,
        "po": 7,
        "sv": 8,
        "gv": 9,
        "vo": 10
    }
```

```md
person_map = 
    {
        "am": 0,
        "ap": 1,
        "tm": 2,
        "tu": 3,
        "ae": 4,
        "in": 5,
        "er": 6,
        "eR": 7,
    }
```

```md
pronoun_map = 
    "pronoun_tag": {
        "Pro.Het": 0,
        "Pro.Pers2": 1,
        "Pro.Pers1": 2,
        "Pro.Pers3": 3,
        "Pro.Dem": 4,
        "Pro.Indef": 5,
        "Pro.Inter": 6,
        "Pro.Rel": 7,
        "Pro.Ref": 8,
        "Pro.Rec": 9,
        "Pro.CoRel": 10,
        "Pro.Rel.CoRel": 11,
        "Pro.Inc": 12,
        "Pro.Pers3.CoRel": 13,
    }
```
```md
number_tag: {"Sing": 0, "Plu": 1},
```
```md
honorificity: {"intimate": 0, "informal": 1, "formal": 2},
```
```md
case: {"genitive": 0, "direct": 1, "objective": 2},
```
```md
proximity: {"proximal": 0, "medial": 1, "distal": 2},
```
