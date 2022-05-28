# Numeric response
The numeric entity has 4 individual fields:

*Literal* : Standard Bengali word for Bengali numerals are given as reponse in this field. For example : `এক`, `সাত` etc.

*Weight* : Any substring added at the end of `Literal` to create an new  Bengali Literal is given as reponse by the *Weight* field. For example : `শ`, `শত` etc.

*Digit* : It identifies the Bengali numerals which are the units of the numeral system. For example : `২`, `৯` etc.

*Suffix* : A letter or group of letters placed after `Literal` or `Digit` are given as response in this field. For example : `টি`, `টা` etc.

Lets understand the numeric response with an example:
```json
{
    "একশত": {
        "Global_Index": [
            [
                0,
                3
            ]
        ],
        "Numeric": {
            "Literal": "এক",
            "Weight": "শত"
        }
    },
    "১টি": {
        "Global_Index": [
            [
                5,
                7
            ]
        ],
        "Numeric": {
            "Digit": "১",
            "Suffix": [
                "টি"
            ]
        }
    }
}
```