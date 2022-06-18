# What does the response mean?

We have 8 different fields in response:

-   _`global_index`_: _global_index_ is an array which contains pairs of starting and ending index of each exact words from given sentence.

-   _`punctuation_flag`_: Will be written

-   _`numeric`_: It identifies the words which contains any kind of numeric entity.[See details here](./numeric.md)
-   _`verb`_: Regonized verb with all its classification are given as response in this entity.
    [See details here](./verbs.md)

-   _`pronoun`_: Will be written
-   _`pos`_: _PoS_ stands for Parts Of Speech. The _PoS_ entity is represented with an array which contains all the possible Parts Of Speech of the word in a sentence.
-   _`Special entity`_: As the name suggests, a _special entity_ can be a special date (for example, ২১ শে ফেব্রুয়ারী which is the International Mother Language Day), a person (for example - ড. মুহাম্মদ জাফর ইকবাল a famous author of science fictions and well-known professor), institute (for example - জাবি which is the abbreviation of Jahangirnagar University) or any other multi-word single entity.

-   _`Composite word`_: Our structural definition of composite Bengali word is -
    prefix (optional) + (One or) Multiple stand-alone Bengali words + suffix (optional)

```json

```
