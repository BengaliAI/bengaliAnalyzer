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

## Local Environment

This is the environment in which the package was developed:

```
 ██████████████████  ████████     Python: 3.9.0
 ██████████████████  ████████     OS: Manjaro 21.2.3 Qonos
 ██████████████████  ████████     Kernel: x86_64 Linux 5.15.21-1-MANJARO
 ██████████████████  ████████     Conda: 4.10.3
 ████████            ████████     CPU: 11th Gen Intel Core i7-11370H @ 8x 4.8GHz
 ████████  ████████  ████████      RAM: 15694MiB
 ████████  ████████  ████████
 ████████  ████████  ████████
 ████████  ████████  ████████
 ████████  ████████  ████████
 ████████  ████████  ████████
 ████████  ████████  ████████
 ████████  ████████  ████████
 ████████  ████████  ████████
```

## Usage

Import the module first.

```python
from bengali_analyzer import bengali_analyzer as bla
```

And then pass the text for analysis.

```python
tokens = bla.analyze_sentence(text)
```

### Response

The response will return `tokens` (data type : `dictionary`) which has each `token` as its `key`. The following dimension will be present for each `token`:

```python
token = {
            "global_index": [int or (int,int)],
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
                "tp": str,
                "non_finite": bool,
                "form": str,
                "related_indices": [int or (int,int)],
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
            "composite_word": {
                "suffix": str,
                "prefix": str,
                "stand_alone_words": set(),
            },
            "special_entity": {
                "definition": str,
                "related_indices": [int or (int,int)],
                "space_indices": set(),
                "suffix": str,
            },
        }
```

## Quick Guide

-   [What does the response mean?](./documentation/response.md)
-   [How does we generate the response?](./documentation/breakdown.md)

## Team

This tool is developed by people with diverse affiliations. The following are the people behind this effort.

| Name                                                                 | Email                        | Affiliation                                          |
| -------------------------------------------------------------------- | ---------------------------- | ---------------------------------------------------- | ------------ | ------------------- | --- | --- | --- | ------------------- | --- | ------------------------------- |
| [Shahriar Elahi Dhruvo]()                                            | shahriardhruvo119@gmail.com  | Shahjalal University of Science & Technology, Sylhet |
| [Md. Rakibul Hasan Ranak](https://www.linkedin.com/in/rakibulranak/) | rakibulhasanranak1@gmail.com | Shahjalal University of Science & Technology, Sylhet |
| [Mahfuzur Rahman Emon]()                                             | emon.swe.sust@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Fazle Rabbi Rakib](https://www.linkedin.com/in/fazle-rakib/)        | fazlerakib009@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Souhardya Saha Dip](https://www.linkedin.com/in/souhardya-saha/)    | souhardyasaha98@gmail.com    | Shahjalal University of Science & Technology, Sylhet | [comment]: # | [Dr. {Farig vai}]() |     |     |     | [Dr. {Mamun sir}]() |     | Jahangirnagar University, Dhaka |
| [Asif Shahriyar Shushmit]()                                          | sushmit@ieee.org             | Bengali.ai                                           |
| [A. A. Noman Ansary](https://www.linkedin.com/in/showrav-ansary/)    | showrav.ansary.bd@gmail.com  |                                                      |

Special thanks to [Md Nazmuddoha Ansary](https://github.com/mnansary) for implementing an open source general purpose `indic grapheme` parser and `bn unicode normalizer`, which are required dependencies in this tool.

In collaboration with: [Bengali.ai](https://bengali.ai/), [SUST](https://www.sust.edu/), [Jahangirnagar University](https://www.jnu.ac.bd/)
