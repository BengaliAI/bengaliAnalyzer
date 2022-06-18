# numeric response

The numeric entity has 4 individual fields:

_Literal_ : Standard Bengali word for Bengali numerals are given as reponse in this field. For example : `এক`, `সাত` etc.

_Weight_ : Any substring added at the end of `literal` to create an new Bengali literal is given as reponse by the _Weight_ field. For example : `শ`, `শত` etc.

_Digit_ : It identifies the Bengali numerals which are the units of the numeral system. For example : `২`, `৯` etc.

_Suffix_ : A letter or group of letters placed after `literal` or `digit` are given as response in this field. For example : `টি`, `টা` etc.

Lets understand the numeric response with an example:

```json
{
    "একশত": {
        "global_index": [[0, 3]],
        "numeric": {
            "literal": "এক",
            "weight": "শত"
        }
    },
    "১টি": {
        "global_index": [[5, 7]],
        "numeric": {
            "digit": "১",
            "suffix": ["টি"]
        }
    }
}
```
