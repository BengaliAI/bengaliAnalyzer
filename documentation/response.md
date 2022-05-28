# What does the response mean?
We have 8 different fields in response:
* *`Global_Index`*: *Global_Index* is an array which contains pairs of starting and ending index of each exact words from given sentence.

* *`Punctuation_Flag`*: Will be written

* *`Numeric`*: It identifies the words which contains any kind of numeric entity.[See details here](./numeric.md)
* *`Verb`*: Regonized verb with all its classification are given as response in this entity.
[See details here](./verbs.md)

* *`Pronoun`*: Will be written
* *`PoS`*: *PoS* stands for Parts Of Speech. The *PoS* entity is represented with an array which contains all the possible Parts Of Speech of the word in a sentence.
* *`Special entity`*: As the name suggests, a *special entity* can be a special date (for example, ২১ শে ফেব্রুয়ারী which is the International Mother Language Day), a person (for example - ড. মুহাম্মদ জাফর ইকবাল a famous author of science fictions and well-known professor), institute (for example - জাবি which is the abbreviation of Jahangirnagar University) or any other multi-word single entity.

* *`Composite word`*: Our structural definition of composite Bengali word is -
Prefix (optional) + (One or) Multiple stand-alone Bengali words + Suffix (optional)

```json

```