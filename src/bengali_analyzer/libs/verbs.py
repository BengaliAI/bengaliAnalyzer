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

        for each in sentence:
            if each not in punctuations:
                tmp += each
        return tmp

    def get_verbs(self, tokens, sentence):
        verb_indexes = []
        sentence = sentence.strip()
        sentence = self.punctuation_remover(sentence)

        sentence_x = sentence
        sentence_x_tokens = sentence_x.split(" ")

        verb = []
        verb_locations = []
        emphasizer_characters = ["ই", "ও"]

        # for handling multi-word verb
        # currently only bigrams are being handled
        for idx, each in enumerate(sentence_x_tokens):
            first = []
            second = []

            bigrams = []
            emphasizer_list = []

            # the list inside the emphasizer list are there
            # incase we need to handle multiple emphasizer later on
            emphasizer = [[None], [None]]

            try:
                first.append(sentence_x_tokens[idx])
                second.append(sentence_x_tokens[idx + 1])

                if first[0][-1] in emphasizer_characters:
                    emphasizer[0] = [first[0][-1]]

                    # keeping the both শুনতেই and শুনতে
                    # to check if both শুনতেই or শুনতে exists in verb-dictionary
                    first.append(first[0][:-1])

                if second[0][-1] in emphasizer_characters:
                    emphasizer[1] = [second[0][-1]]

                    # keeping the both শুনতেই and শুনতে
                    # to check if both শুনতেই or শুনতে exists in verb-dictionary
                    second.append(second[0][:-1])

                # creating bigrams with every possible combination
                for i, f in enumerate(first):
                    for j, s in enumerate(second):
                        bigrams.append(f + " " + s)

                        emphasizer_list.append(
                            [
                                (lambda: [None], lambda: emphasizer[0])[
                                    i == 0](),
                                (lambda: [None], lambda: emphasizer[1])[
                                    j == 0](),
                            ]
                        )

                # checking if any bigram represents verb
                # if so then the emphasizer char is being tracked
                for each in bigrams:
                    if each in self.data2["word"].values:
                        verb_locations.append(
                            {
                                "verb": each,
                                "location": [idx, idx + 1],
                                "emphasizer": emphasizer_list[0],
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
            emphasizer = [[None]]

            # check verb which last char doesn't emphasize, that emphasizer char is part of the word
            if each in self.data1["word"].values:
                verb_locations.append(
                    {
                        "verb": each,
                        "location": [idx],
                        "emphasizer": emphasizer,
                        "original_verb": each,
                    }
                )

            # removing last char if it is an emphasis char, and checking the word without it
            lastChar = each[-1]
            original_verb = each

            if lastChar in emphasizer_characters:
                each = each[:-1]
                emphasizer = [[lastChar]]

            # check verb which last char does emphasize
            if each in self.data1["word"].values:
                verb_locations.append(
                    {
                        "verb": each,
                        "location": [idx],
                        "emphasizer": emphasizer,
                        "original_verb": original_verb,
                    }
                )

        # generating information for every found verbs
        for each in verb_locations:
            info = self.data[self.data["word"] == each["verb"]]

            tense_person_emp = []

            for eachx in zip(info["tense"], info["person"]):
                tense_person_emp.append(
                    {
                        "tense": eachx[0],
                        "person": eachx[1],
                        "emphasizer": each["emphasizer"],
                    }
                )

            verb.append(
                {
                    "Index": each["location"],
                    "original_word": each["original_verb"],
                    "Parent_Verb": info["parent_word"].iloc[0],
                    "TPE": tense_person_emp,
                    "Language_Form": "standard",
                }
            )

        flag = []
        for x in verb:
            keys = []
            index = []
            x_bar = x["original_word"].split(" ")

            for y in x_bar:
                keys.append(y)
                flag.extend(tokens[y]["Global_Index"])
                index.extend(tokens[y]["Global_Index"])

            for y in keys:
                if len(index) > 1:
                    tokens[y]["Verb"]["Related_Indices"].append(index)

                tokens[y]["Verb"]["TPE"] = x["TPE"]
                tokens[y]["Verb"]["Parent_Verb"] = x["Parent_Verb"]
                tokens[y]["Verb"]["Language_Form"] = x["Language_Form"]

        return verb_indexes

    # print(sentence)
    # verb_lemmatizer(sentence)
