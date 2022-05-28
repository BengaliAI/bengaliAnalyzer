# Bengali (Bangla) Analyzer

This package provides an analyzer for Bengali (Bangla) language. We have gone through a dictionary entry based approach with grammatical sanitizing for this project. Here in our implementation we have 5 different type of entities:
* *Prefix*: *Prefix* or *উপসর্গ* is a substring in a word that generally does not hold a meaning of its own but when added to a word that has its own meaning, gets a new definition on it.

* *Suffix*: *Suffix* or *অনুসর্গ* is a trailing substring in a word that generally does not hold a meaning of its own but when added to a word that has its own meaning, gets a new definition on it.

* *Verb*: Any word or group of words that describe the action, state or occurrence of an event in a Bengali sentence. For example - খাওয়া, চলে যাওয়া etc. etc
.
* *Non-verb*: Any other remaining parts of speech that are not recognized as a verb in a Bengali sentence. For example - আমি, খুব, তারা, বাংলা, বয়স, etc. etc.

* *Special entity*: As the name suggests, a *special entity* can be a special date (for example, ২১ শে ফেব্রুয়ারী which is the International Mother Language Day), a person (for example - ড. মুহাম্মদ জাফর ইকবাল a famous author of science fictions and well-known professor), institute (for example - জাবি which is the abbreviation of Jahangirnagar University) or any other multi-word single entity.

* *Composite word*: Our structural definition of composite Bengali word is -
Prefix (optional) + (One or) Multiple stand-alone Bengali words + Suffix (optional)


Our package analyzes the given text and returns the word configurations of the text according to the definitions we have chosen to give to the entities which could be present in a bengali sentence.

## Installation
The package can be installed in any fashion. It is highly recommended to install [Conda](https://conda.io/) and then run the following command to install the package:

`pip install bengalianlyzer`

## Local Environment
This is the environment in which the package was developed:
```
 ██████████████████  ████████     Python: 3.9.0
 ██████████████████  ████████     OS: Manjaro 21.2.3 Qonos
 ██████████████████  ████████     Kernel: x86_64 Linux 5.15.21-1-MANJARO
 ██████████████████  ████████     Conda: 4.10.3
 ████████            ████████     CPU: 11th Gen Intel Core i7-11370H @ 8x 4.8GHz 
 ████████  ████████  ████████     GPU: NVIDIA GeForce RTX 3060 Laptop GPU
 ████████  ████████  ████████     RAM: 15694MiB
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
from bengalianalyzer import BengaliAnalyzer 
```
And then pass the text for analysis.
```python
bl = BengaliAnalyzer()
tokens = bl.analyze_sentence(text)
```
### Response
The response will return `tokens` (data type : `dictionary`) which has each `token` as its `key`. The following dimension will be present for each `token`:

```python
tokens[token] = {
            "Global_Index": [int or (int, int)],
            "Punctuation_Flag": bool,
            "Numeric":
                {
                    "Digit": int,
                    "Literal": str,
                    "Weight": str,
                    "Suffix": [str]
                },
            "Verb":
                {
                    "Parent_Verb": str,
                    "Tense": str,
                    "Emphasis": [str],
                    "Form": str,
                    "Person": str,
                    "Related_Indices": [[int or (int,int)]]
                },
            "Non_Verb": str,
            "Composite_Word":
                {
                    "Suffix": str,
                    "Prefix": str,
                    "Stand_Alone_Words": {str},
                },
            "Special_Entity":
                {
                    "Definition": str,
                    "Related_Indices": [[int or (int,int)]]
                }
        }
```

## Quick Guide
- [What does the response mean?](./documentation/response.md)
- [How does we generate the response?](./documentation/breakdown.md)

## Team
This tool is developed by people with diverse affiliations. The following are the people behind this effort.

| Name                                                                 | Email                        | Affiliation                                          |
|----------------------------------------------------------------------|------------------------------|------------------------------------------------------|
| [Shahriar Elahi Dhruvo]()                                            | shahriardhruvo119@gmail.com  | Shahjalal University of Science & Technology, Sylhet |
| [Md. Rakibul Hasan Ranak](https://www.linkedin.com/in/rakibulranak/) | rakibulhasanranak1@gmail.com | Shahjalal University of Science & Technology, Sylhet |
| [Mahfuzur Rahman Emon]()                                             | emon.swe.sust@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Fazle Rabbi Rakib](https://www.linkedin.com/in/fazle-rakib/)        | fazlerakib009@gmail.com      | Shahjalal University of Science & Technology, Sylhet |
| [Souhardya Saha Dip](https://www.linkedin.com/in/souhardya-saha/)    | souhardyasaha98@gmail.com    | Shahjalal University of Science & Technology, Sylhet |[comment]: #| [Dr. {Farig vai}]()                                                  |||| [Dr. {Mamun sir}]()                                                  |      | Jahangirnagar University, Dhaka                      |
| [Asif Shahriyar Shushmit]()                                          | sushmit@ieee.org             | Bengali.ai                                           |
| [A. A. Noman Ansary](https://www.linkedin.com/in/showrav-ansary/)                                               | showrav.ansary.bd@gmail.com  | Govt. Laboratory High School, Rajshahi               |

Special thanks to [Md Nazmuddoha Ansary](https://github.com/mnansary) for implementing an open source general purpose `indic grapheme` parser, which is a required dependency in this tool. 

In collaboration with: [Bengali.ai](https://bengali.ai/), [SUST](https://www.sust.edu/), [RGLHS](http://rglhs.edu.bd/), [Jahangirnagar University](https://www.jnu.ac.bd/)