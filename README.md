# Bengali (Bangla) Analyzer

This package provides an analyzer for Bengali (Bangla) language. We have gone through a dictionary entry based approach with grammatical sanitizing for this project. Here in our implementation we have 5 different type of entities:

-   _Prefix_: _Prefix_ or _উপসর্গ_ is a substring in a word that generally does not hold a meaning of its own but when added to a word that has its own meaning, gets a new definition on it.

-   _Suffix_: _Suffix_ or _অনুসর্গ_ is a trailing substring in a word that generally does not hold a meaning of its own but when added to a word that has its own meaning, gets a new definition on it.

-   _Verb_: Any word or group of words that describe the action, state or occurrence of an event in a Bengali sentence. For example - খাওয়া, চলে যাওয়া etc. etc
    .
-   _Non-verb_: Any other remaining parts of speech that are not recognized as a verb in a Bengali sentence. For example - আমি, খুব, তারা, বাংলা, বয়স, etc. etc.

-   _Special entity_: As the name suggests, a _special entity_ can be a special date (for example, ২১ শে ফেব্রুয়ারী which is the International Mother Language Day), a person (for example - ড. মুহাম্মদ জাফর ইকবাল a famous author of science fictions and well-known professor), institute (for example - জাবি which is the abbreviation of Jahangirnagar University) or any other multi-word single entity.

-   _Composite word_: Our structural definition of composite Bengali word is -
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

-   For text analyzing: [(Preview method details)](./documentation/analyze_sentence.md)

```python
tokens = bla.analyze_sentence(text)
```

-   For Parts of Speech tagging:

```python
tokens = bla.analyze_pos(text)
```

-   For lemma parsing:

```python
tokens = bla.lemmatize_sentence(text)
```

-   For voctorized form: [(Preview method details)](./documentation/vectorized_pos.md)

```python
tokens = bla.vectorize_pos(text)
```

### Response

-   For `analyze_sentence(text)` :

Structure:

```python
token = {
            "numeric_flag": bool,
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
text: "অর্থনীতিবিদদের ভালো কাজ দেয়া উচিত।"

response:
{'অর্থনীতিবিদদের': {'numeric_flag': False,
'global_index': [[0, 13]],
'pos': ['বিশেষ্য'],
'composite_flag': False,
'composite_word': {'suffix': 'দের',
'stand_alone_words': ['অর্থ', 'নীতি', 'বিদ']}},
'ভালো': {'numeric_flag': False,
'global_index': [[15, 18]],
'verb': {'parent_verb': ['ভালা'],
'tp': [{'tense': 'bo', 'person': 'tm'}, {'tense': 'sb', 'person': 'tm'}],
'related_indices': [[15, 18]],
'language_form': 'standard'},
'pos': ['বিশেষ্য', 'বিশেষণ', 'অব্যয়'],
'composite_flag': False},
'কাজ': {'numeric_flag': False,
'global_index': [[20, 22]],
'pos': ['বিশেষ্য'],
'composite_flag': False},
'দেয়া': {'numeric_flag': False,
'global_index': [[24, 27]],
'verb': {'parent_verb': ['দেয়ানো'],
'tp': [{'tense': 'bo', 'person': 'tu'}],
'related_indices': [[24, 27]],
'language_form': 'standard'},
'pos': ['বিশেষ্য'],
'composite_flag': False},
'উচিত': {'numeric_flag': False,
'global_index': [[29, 32]],
'pos': ['বিশেষণ'],
'composite_flag': False},
'।': {'numeric_flag': False,
'global_index': [[33, 33]],
'punctuation_flag': True,
'pos': ['punc'],
'composite_flag': False}}
```

-   For `analyze_pos(text)`:
    The the mother list will contain all the tokens and each child list contains the `PoS` taggings of that token.

Structure :

```python
dict(str:dict(str:list()))
```

Example:

```md
text: "আমার ফ্যামিলি প্রবলেমের কারণে কুয়েটে পড়াই হবে না কিন্তু টিউশন করে সাপোর্ট লাগবে এজন্য চুয়েট চুজ করা ভুল হবে? খেতে থাকবই খেতে থাকব"

response:
{'আমার': {'pos': ['pronoun']},
'ফযামিলি': {'pos': ['undefined']},
'প্রবলেমের': {'pos': ['undefined']},
'কারণে': {'pos': ['undefined']},
'কুয়েটে': {'pos': ['undefined']},
'পড়াই': {'pos': ['verb']},
'হবে': {'pos': ['verb']},
'না': {'pos': ['conjunction', 'noun']},
'কিন্তু': {'pos': ['conjunction']},
'টিউশন': {'pos': ['undefined']},
'করে': {'pos': ['verb']},
'সাপোর্ট': {'pos': ['undefined']},
'লাগবে': {'pos': ['verb']},
'এজন্য': {'pos': ['conjunction', 'adverb']},
'চুয়েট': {'pos': ['undefined']},
'চুজ': {'pos': ['undefined']},
'করা': {'pos': ['verb']},
'ভুল': {'pos': ['adjective', 'noun']},
'?': {'pos': ['punctuation']},
'খেতে থাকবই': {'pos': ['contentative_verb']},
'খেতে থাকব': {'pos': ['contentative_verb']}}
```

-   For `lemmatize_sentence(text)`:

Structure :

```python
list(list())
```

Example:

```md
text : "অর্থনীতিবিদদের ভালো কাজ দেয়া উচিত।"
respone : ['অর্থনীতিবিদ', 'ভালা/ভালো, 'কাজ', 'দেয়ানো', 'উচিত', '।']
```

-   For `vectorize_pos(text)`:

Structure :

```python
dict(str:list(list()))
```

Example:

```md
text : "ঢাকা অর্থনৈতিক রাজধানী।"
respone : 
{'ঢাকা': [[[4, 185, 3, 3, False]],[1, None, None],[0, None, None],[5, None, None]],
 'অর্থনৈতিক': [[0, None, None]],
 'রাজধানী': [[1, None, None]]
 '।': [[6, None, None]]}
```

## Quick Guide

-   [What does the response mean?](./documentation/response.md)
-   [How do we generate the response?](./documentation/breakdown.md)

## Team

This tool is developed by people with diverse affiliations. The following are the people behind this effort.

| Name                                                                                      | Email                        | Affiliation                                          |
| ----------------------------------------------------------------------------------------- | ---------------------------- | ---------------------------------------------------- |
| [Shahriar Elahi Dhruvo](https://www.linkedin.com/in/shahriardhruvo/)                      | shahriardhruvo119@gmail.com  | Shahjalal University of Science & Technology, Sylhet |
| [Md. Rakibul Hasan](https://www.linkedin.com/in/rakibulranak/)                            | rakibulhasanranak1@gmail.com | Shahjalal University of Science & Technology, Sylhet |
| [Mahfuzur Rahman Emon](https://www.linkedin.com/in/emon-swe-sust/)                        | emon.swe.sust@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Fazle Rabbi Rakib](https://www.linkedin.com/in/fazle-rakib/)                             | fazlerakib009@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Souhardya Saha Dip](https://www.linkedin.com/in/souhardya-saha/)                         | souhardyasaha98@gmail.com    | Shahjalal University of Science & Technology, Sylhet |
| [Dr. Farig Yousuf Sadeque](https://www.bracu.ac.bd/about/people/farig-yousuf-sadeque)     | farigsadeque@gmail.com       | BRAC University, Dhaka                               |
| [Mohammad Mamun Or Rashid](https://www.linkedin.com/in/mohammad-mamun-or-rashid-57207541) | mamunbd@juniv.edu            | Jahangirnagar University, Dhaka                      |
| [Asif Shahriyar Shushmit](https://bd.linkedin.com/in/sushmit109)                          | sushmit@ieee.org             | Bengali.ai                                           |
| [A. A. Noman Ansary](https://www.linkedin.com/in/showrav-ansary/)                         | showrav.ansary.bd@gmail.com  | BRAC University, Dhaka                               |
| [Sazia Mehnaz](https://www.linkedin.com/in/sazia-mehnaz-196756202)                        | sayma.iict@gmail.com         | Bengali.ai                                           |

Special thanks to [Md Nazmuddoha Ansary](https://github.com/mnansary) for implementing an open source general purpose [`indic grapheme parser`](https://github.com/mnansary/indicparser) and [`bn unicode normalizer`](https://github.com/mnansary/bnUnicodeNormalizer), which are required dependencies in this tool.

In collaboration with: [Bengali.ai](https://bengali.ai/), [SUST](https://www.sust.edu/), [Jahangirnagar University](https://www.jnu.ac.bd/), [BRAC University](https://www.bracu.ac.bd)
