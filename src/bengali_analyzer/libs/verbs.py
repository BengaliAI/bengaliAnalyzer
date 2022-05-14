# high_classic = shadhu
# prescriptive_standard = cholito (dictionary)
# tolerable_alternative = kortesilam
# colloquial = koiralchi


# শুনতেই থাকবে। *** এটা নাই

# sentence = 'থাকবে আউলাই শুনতে থাকবে আউলানো'
# sentence = 'থাকবে আউলাই শুনতেই থাকবে আউলানো'
# sentence = 'আমার কথা শুনতে শুনতে তুমি ঢাকায় থাকবে'
# sentence = 'আমার কথা শুনতেই শুনতেই তুমি ঢাকায় থাকবেও দেও'


# sentence = 'সে আমার কথা শুনতেই থাকবে'
# sentence = 'আমি হাঁটতে, হাঁটতেই ঐখানে যেয়ে ঘুমিয়ে গিয়েছিলাম!'


class VerbAnalyzer:
    def __init__(self, data, data1, data2):
        self.data = data
        self.data1 = data1
        self.data2 = data2

        self.verb_form_mapper = {
            "tense": {
                "sb": "সাধারণ বর্তমান",
                "gb": "ঘটমান বর্তমান",
                "pb": "পুরাঘটিত বর্তমান",
                "bo": "বর্তমান অনুজ্ঞা",
                "so": "সাধারণ অতীত",
                "no": "নিত্যবৃত্ত অতীত",
                "go": "ঘটমান অতীত",
                "po": "পুরাঘটিত অতীত",
                "sv": "সাধারণ ভবিষ্যত",
                "gv": "ঘটমান ভবিষ্যত",
                "vo": "ভবিষ্যত অনুজ্ঞা",
            },
            "person": {
                "am": "আমি/আমরা",
                "ap": "আপনি/আপনারা",
                "tm": "তুমি/তোমরা",
                "tu": "তুই/তোরা",
                "ae": "এ/ও/যে/সে",
                "in": "ইনি/উনি/তিনি/যিনি",
                "er": "এরা/ওরা/তারা/যারা",
                "eR": "এঁরা/ওঁরা/তাঁরা/যাঁরা",
            },
        }

    @staticmethod
    def punctuation_remover(sentence):
        tmp = ""
        punctuations = [
            ".",
            ",",
            ";",
            ":",
            "!",
            "?",
            '"',
            "'",
            "`",
            "~",
            "^",
            "*",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            "।",
        ]

        for idx, each in enumerate(sentence):
            if each not in punctuations:
                tmp += each
        return tmp

    def get_verbs(self, tokens, sentence):
        # print("----------GET VERB-----------")

        verb_indexes = []

        sentence = sentence.strip()

        sentence = self.punctuation_remover(sentence)

        sentence_x = sentence
        sentence_x_tokens = sentence_x.split(" ")

        verb = []
        verb_locations = []
        emphasis_characters = ["ই", "ও"]

        # for handling multi-word verb
        # currently only bigrams are being handled
        for idx, each in enumerate(sentence_x_tokens):
            first = []
            second = []

            bigrams = []
            emphasis_list = []

            # the list inside the emphasis list are there
            # incase we need to handle multiple emphasizer later on
            emphasis = [[None], [None]]

            try:
                first.append(sentence_x_tokens[idx])
                second.append(sentence_x_tokens[idx + 1])

                if first[0][-1] in emphasis_characters:
                    emphasis[0] = [first[0][-1]]

                    # keeping the both শুনতেই and শুনতে
                    # to check if both শুনতেই or শুনতে exists in verb-dictionary
                    first.append(first[0][:-1])

                if second[0][-1] in emphasis_characters:
                    emphasis[1] = [second[0][-1]]

                    # keeping the both শুনতেই and শুনতে
                    # to check if both শুনতেই or শুনতে exists in verb-dictionary
                    second.append(second[0][:-1])

                # creating bigrams with every possible combination
                for i, f in enumerate(first):
                    for j, s in enumerate(second):
                        bigrams.append(f + " " + s)

                        emphasis_list.append(
                            [
                                (lambda: [None], lambda: emphasis[0])[i == 0](),
                                (lambda: [None], lambda: emphasis[1])[j == 0](),
                            ]
                        )

                # checking if any bigram represents verb
                # if so then the emphasis char is being tracked
                for each in bigrams:
                    if each in self.data2["word"].values:
                        verb_locations.append(
                            {
                                "verb": each,
                                "location": [idx, idx + 1],
                                "emphasis": emphasis_list[0],
                                "original_verb": bigrams[0],
                            }
                        )
                        sentence_x = sentence_x.replace(each, "x x")

                        break
            except:
                continue

        sentence_x_tokens = sentence_x.split(" ")

        # for handling single-word verb
        for idx, each in enumerate(sentence_x_tokens):
            emphasis = [[None]]

            # check verb which last char doesn't emphasize, that emphasis char is part of the word
            if each in self.data1["word"].values:
                verb_locations.append(
                    {
                        "verb": each,
                        "location": [idx],
                        "emphasis": emphasis,
                        "original_verb": each,
                    }
                )

            # removing last char if it is an emphais char and checking the word without it
            lastChar = each[-1]
            original_verb = each

            if lastChar in emphasis_characters:
                each = each[:-1]
                emphasis = [[lastChar]]

            # check verb which last char does emphasize
            if each in self.data1["word"].values:
                verb_locations.append(
                    {
                        "verb": each,
                        "location": [idx],
                        "emphasis": emphasis,
                        "original_verb": original_verb,
                    }
                )

        # generating information for every found verbs
        for each in verb_locations:
            info = self.data[self.data["word"] == each["verb"]]
            tense_person_emp = []

            for eachx in zip(info["tense"], info["person"]):
                tense_person_emp.append(eachx + tuple(each["emphasis"]))

            verb.append(
                {
                    "Index": each["location"],
                    "original_word": each["original_verb"],
                    "Parent_Verb": info["parent_word"].iloc[0],
                    "Tense_Person_Emphasis": tense_person_emp,
                    "Language_Form": "standard",
                }
            )

        flag = []
        for x in verb:
            index = []
            keys = []
            x_bar = x["original_word"].split(" ")

            for y in x_bar:
                keys.append(y)
                flag.extend(tokens[y]["Global_Index"])
                index.extend(tokens[y]["Global_Index"])

            for y in keys:
                if len(index) > 1:
                    tokens[y]["Verb"]["Related_Indices"].append(index)

                tokens[y]["Verb"]["Parent_Verb"] = x["Parent_Verb"]
                tokens[y]["Verb"]["Tense_Person_Emphasis"] = x["Tense_Person_Emphasis"]
                tokens[y]["Verb"]["Language_Form"] = x["Language_Form"]

        return verb_indexes

    # print(sentence)
    # verb_lemmatizer(sentence)
