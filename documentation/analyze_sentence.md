## analyze_sentence(text, isReturnTypeSimplified = True)

By default, `analyze_sentence(text)` return a simplied response :
```json
{
   "ঢাকা":{
      "numeric_flag":false,
      "global_index":[
         [
            0,
            3
         ]
      ],
      "verb":{
         "parent_verb":[
            "ঢাকানো"
         ],
         "tp":[
            {
               "tense":"bo",
               "person":"tu"
            }
         ],
         "non_finite":true,
         "related_indices":[
            [
               0,
               3
            ]
         ],
         "language_form":"standard"
      },
      "pos":[
         "ক্রিয়া",
         "বিশেষ্য",
         "বিশেষণ",
         "ক্রিয়াবিশেষ্য"
      ],
      "composite_flag":false
   }
}
```

`analyze_sentence(text, False)` will return a detailed response :
```json
{
    "ঢাকা": {
        "numeric_flag": false,
        "global_index": [
            [
                0,
                3
            ]
        ],
        "punctuation_flag": false,
        "numeric": {
            "digit": null,
            "literal": null,
            "weight": null,
            "suffix": []
        },
        "verb": {
            "parent_verb": [
                "ঢাকানো"
            ],
            "emphasizer": [
                null
            ],
            "tp": [
                {
                    "tense": "bo",
                    "person": "tu"
                }
            ],
            "non_finite": true,
            "contentative_verb": false,
            "negation": false,
            "form": null,
            "related_indices": [
                [
                    0,
                    3
                ]
            ],
            "language_form": "standard"
        },
        "pronoun": {
            "pronoun_tag": null,
            "number_tag": null,
            "honorificity": null,
            "case": null,
            "proximity": null,
            "encoding": null
        },
        "pos": [
            "ক্রিয়া",
            "বিশেষ্য",
            "বিশেষণ",
            "ক্রিয়াবিশেষ্য"
        ],
        "composite_flag": false,
        "composite_word": {
            "suffix": null,
            "prefix": null,
            "stand_alone_words": []
        },
        "special_entity": {
            "definition": null,
            "related_indices": [],
            "space_indices": [],
            "suffix": null
        }
    }
}
```