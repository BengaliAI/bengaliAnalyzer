# Bengali (Bangla) Analyzer

This package provides an analyzer for Bengali (Bangla) language. We have gone through a dictionary entry based approach with grammatical sanitizing for this project. Here in our implementation we have 5 different type of entities:

- _Prefix_: _Prefix_ or _উপসর্গ_ is a substring in a word that generally does not hold a meaning of its own but when added to a word that has its own meaning, gets a new definition on it.

- _Suffix_: _Suffix_ or _অনুসর্গ_ is a trailing substring in a word that generally does not hold a meaning of its own but when added to a word that has its own meaning, gets a new definition on it.

- _Verb_: Any word or group of words that describe the action, state or occurrence of an event in a Bengali sentence. For example - খাওয়া, চলে যাওয়া etc. etc
    .
- _Non-verb_: Any other remaining parts of speech that are not recognized as a verb in a Bengali sentence. For example - আমি, খুব, তারা, বাংলা, বয়স, etc. etc.

- _Special entity_: As the name suggests, a _special entity_ can be a special date (for example, ২১ শে ফেব্রুয়ারী which is the International Mother Language Day), a person (for example - ড. মুহাম্মদ জাফর ইকবাল a famous author of science fictions and well-known professor), institute (for example - জাবি which is the abbreviation of Jahangirnagar University) or any other multi-word single entity.

- _Composite word_: Our structural definition of composite Bengali word is -
    prefix (optional) + (One or) Multiple stand-alone Bengali words + suffix (optional)

Our package analyzes the given text and returns the word configurations of the text according to the definitions we have chosen to give to the entities which could be present in a bengali sentence.

## Installation

The package can be installed in any fashion. It is highly recommended to install [Conda](https://conda.io/) and then run the following command to install the package:

`pip install bengalianalyzer`

Or,

1. Download the whole repo as a compressed file.
2. Extract the compressed file.
3. Open a terminal at the base directory of the extracted folder.
4. Type `pip install .` and hit enter.

## Local Environment

This is the environment in which the package was developed:

```md
Python: 3.9.0
OS: Manjaro 21.2.3 Qonos
Kernel: x86_64 Linux 5.15.21-1-MANJARO
Conda: 4.10.3
CPU: 11th Gen Intel Core i7-11370H @ 8x 4.8GHz
RAM: 15694MiB
```

## Usage

Import the module first.

```python
from bengali_analyzer import bengali_analyzer as bla
```

And then pass the text for analysis.

- For text analyzing:

```python
tokens = bla.analyze_sentence(text)
```

- For Parts of Speech tagging:

```python
tokens = bla.analyze_pos(text)
```

- For lemma parsing:

```python
tokens = bla.lemmatize_sentence(text)
```

### Response

- For `analyze_sentence(text)` :

Structure:

```python
token = {
            "global_index": [(int,int)],
            "punctuation_flag": bool,
            "numeric": {
                "digit": int,
                "literal": str,
                "weight": str,
                "suffix": [str]
            },
            "verb": {
                "parent_verb": str,
                "emphasizer": str,
                "contentative_verb": bool,
                "tp": str,
                "non_finite": bool,
                "form": str,
                "related_indices": [(int,int)],
            },
            "pronoun": {
                "pronoun_tag": str,
                "number_tag": str,
                "honorificity": str,
                "case": str,
                "proximity": str,
                "encoding": str,
            },
            "pos": [str],
            "composite_flag": bool,
            "composite_word": {
                "suffix": str,
                "prefix": str,
                "stand_alone_words": set(),
            },
            "special_entity": {
                "definition": str,
                "related_indices": [(int,int)],
                "space_indices": set(),
                "suffix": str,
            },
        }
```

Example:

```md
text: "২১শে বক বোকাদের একটা ভাল দিন?"

response:
{'২১শে': {'global_index': [[0, 3]],
  'numeric': {'digit': '২১', 'weight': 'শ', 'suffix': ['ে']},
  'composite_flag': False,
  'special_entity': {'related_indices': [[0, 3], [5, 6], [8, 14]],
   'space_indices': [4, 7]}},
 'বক': {'global_index': [[5, 6]],
  'pos': ['বিশেষ্য'],
  'composite_flag': False,
  'special_entity': {'related_indices': [[0, 3], [5, 6], [8, 14]],
   'space_indices': [4, 7]}},
 'বোকাদের': {'global_index': [[8, 14]],
  'composite_flag': False,
  'special_entity': {'related_indices': [[0, 3], [5, 6], [8, 14]],
   'space_indices': [4, 7],
   'suffix': 'দের'}},
 'একটা': {'global_index': [[16, 19]],
  'numeric': {'literal': 'এক', 'suffix': ['টা']},
  'pronoun': {'pronoun_tag': 'Pro.Indef', 'number_tag': 'Sing'},
  'pos': ['বিশেষণ'],
  'composite_flag': False},
 'ভাল': {'global_index': [[21, 23]],
  'verb': {'parent_verb': ['ভালা'],
   'tp': [{'tense': 'bo', 'person': 'tu'}],
   'related_indices': [[21, 23]],
   'Language_Form': 'standard'},
  'pos': ['বিশেষ্য'],
  'composite_flag': False},
 'দিন': {'global_index': [[25, 27]],
  'verb': {'parent_verb': ['দেওয়া'],
   'tp': [{'tense': 'bo', 'person': 'ap'}],
   'related_indices': [[25, 27]],
   'Language_Form': 'standard'},
  'pos': ['বিশেষ্য'],
  'composite_flag': False,
  'special_entity': {'related_indices': [[25, 27]]}},
 '?': {'global_index': [[28, 28]],
  'punctuation_flag': True,
  'pos': ['punc'],
  'composite_flag': False}}
```

- For `analyze_pos(text)`:
The the mother list will contain all the tokens and each child list contains the `PoS` taggins of that token.

Structure :

```python
list(list())
```

Example:

```md
text: "আমার ফ্যামিলি প্রবলেমের কারণে কুয়েটে পড়াই হবে না কিন্তু টিউশন করে সাপোর্ট লাগবে এজন্য চুয়েট চুজ করা ভুল হবে? খেতে থাকবই খেতে থাকব"

response:
[['pronoun', 'pronoun'],
 ['undefined'],
 ['undefined'],
 ['undefined'],
 ['undefined'],
 ['verb', 'finite_verb', 'non_finite_verb'],
 ['verb', 'verb', 'finite_verb'],
 ['conjunction', 'noun'],
 ['conjunction'],
 ['undefined'],
 ['verb', 'finite_verb', 'non_finite_verb'],
 ['undefined'],
 ['verb', 'finite_verb'],
 ['conjunction', 'adverb'],
 ['undefined'],
 ['undefined'],
 ['adverb', 'finite_verb', 'non_finite_verb'],
 ['noun', 'adjective'],
 ['verb', 'verb', 'finite_verb'],
 ['punctuation'],
 ['verb', 'verb', 'finite_verb', 'non_finite_verb'],
 ['verb', 'verb', 'finite_verb', 'non_finite_verb']]
```

- For `lemmatize_sentence(text)`:
Structure :

```python
list(list())
```

Example:

```md
text : "অর্থনীতিবিদদের ভালো কাজ দেয়া উচিত।"
respone : [['অর্থনীতিবিদ'], ['ভালা'], ['কাজ'], ['দেয়ানো'], ['উচিত'], ['।']]
```

## Quick Guide

- [What does the response mean?](./documentation/response.md)
- [How do we generate the response?](./documentation/breakdown.md)

## Team

This tool is developed by people with diverse affiliations. The following are the people behind this effort.

| Name                                                                 | Email                        | Affiliation                                          |
|----------------------------------------------------------------------|------------------------------|------------------------------------------------------|
| [Shahriar Elahi Dhruvo](https://www.linkedin.com/in/shahriardhruvo/)                                            | shahriardhruvo119@gmail.com  | Shahjalal University of Science & Technology, Sylhet |
| [Md. Rakibul Hasan Ranak](https://www.linkedin.com/in/rakibulranak/) | rakibulhasanranak1@gmail.com | Shahjalal University of Science & Technology, Sylhet |
| [Mahfuzur Rahman Emon](https://www.linkedin.com/in/emon-swe-sust/)                                             | emon.swe.sust@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Fazle Rabbi Rakib](https://www.linkedin.com/in/fazle-rakib/)        | fazlerakib009@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Souhardya Saha Dip](https://www.linkedin.com/in/souhardya-saha/)    | souhardyasaha98@gmail.com    | Shahjalal University of Science & Technology, Sylhet |
| [Dr. Farig Yousuf Sadeque](https://www.bracu.ac.bd/about/people/farig-yousuf-sadeque)|farigsadeque@gmail.com | BRAC University, Dhaka|
| [Mohammad Mamun Or Rashid](https://www.linkedin.com/in/mohammad-mamun-or-rashid-57207541)                                                  |   mamunbd@juniv.edu   | Jahangirnagar University, Dhaka                      |
| [Asif Shahriyar Shushmit](https://bd.linkedin.com/in/sushmit109)                                          | sushmit@ieee.org             | Bengali.ai                                           |
| [A. A. Noman Ansary](https://www.linkedin.com/in/showrav-ansary/)                                               | showrav.ansary.bd@gmail.com  | BRAC University, Dhaka|

Special thanks to [Md Nazmuddoha Ansary](https://github.com/mnansary) for implementing an open source general purpose [`indic grapheme parser`](https://github.com/mnansary/indicparser) and [`bn unicode normalizer`](https://github.com/mnansary/bnUnicodeNormalizer), which are required dependencies in this tool.

In collaboration with: [Bengali.ai](https://bengali.ai/), [SUST](https://www.sust.edu/), [Jahangirnagar University](https://www.jnu.ac.bd/), [BRAC University](https://www.bracu.ac.bd)
