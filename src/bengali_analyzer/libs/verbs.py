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


from tkinter.tix import Tree


class VerbAnalyzer:
    def __init__(self, data, data1, data2, non_finite_verbs):
        self.data = data
        self.data1 = data1
        self.data2 = data2
        self.non_finite_verbs = non_finite_verbs

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
        emphasizer_list = []
        emphasizer_characters = ["ই", "ও"]
        non_finte = dict()

        # for handling multi-word verb
        # currently only bigrams are being handled
        for idx, each in enumerate(sentence_x_tokens):
            first = []
            second = []
            emphasizer_list_temp = []

            bigrams = []

            # the list inside the emphasizer list are there
            # incase we need to handle multiple emphasizer later on
            emphasizer = [[None], [None]]

            try:
                first.append(sentence_x_tokens[idx])
                # question by ranak > what if [idx+1] > out of index
                second.append(sentence_x_tokens[idx + 1])

                if first[0][-1] in emphasizer_characters:
                    emphasizer[0] = [first[0][-1]]

                    # keeping the both শুনতেই and শুনতে
                    # to check if both শুনতেই or শুনতে exists in verb-dictionaryƒ
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
                        if bigrams[-1] in self.data2["word"].values:
                            em1 = [None]
                            em2 = [None]
                            if (f != first[0]):
                                em1 = emphasizer[0]
                            if(s != second[0]):
                                em2 = emphasizer[1]
                            emphasizer_list.append([em1, em2])
                            verb_locations.append(
                                {
                                    "verb": bigrams[-1],
                                    "location": [idx, idx + 1],
                                    "original_verb": bigrams[0],
                                }
                            )
                            non_finte[len(verb_locations)-1] = [False, True]
                            sentence_x = sentence_x.replace(bigrams[0], "x x")
                            break
            except:
                continue

        sentence_x_tokens = sentence_x.split(" ")

        # for handling single-word verb
        emphasizer = [[None]]
        for idx, each in enumerate(sentence_x_tokens):

            # check verb which last char doesn't emphasize, that emphasizer char is part of the word
            alreadyFound = False
            if each in self.data1["word"].values:
                alreadyFound = True
                emphasizer_list.append(emphasizer)
                verb_locations.append(
                    {
                        "verb": each,
                        "location": [idx],
                        "original_verb": each,
                    }
                )

            if not alreadyFound:
                # removing last char if it is an emphasis char, and checking the word without it
                lastChar = each[-1]

                if lastChar in emphasizer_characters:
                    temp = each[:-1]

                    # check verb which last char does emphasize
                    if temp in self.data1["word"].values:
                        emphasizer = [[lastChar]]
                        emphasizer_list.append(emphasizer)
                        alreadyFound = True
                        verb_locations.append(
                            {
                                "verb": temp,
                                "location": [idx],
                                "original_verb": each,
                            }
                        )
            non_F = False
            if alreadyFound:
                if each in self.non_finite_verbs["word"].values or (each[-1] in emphasizer_characters and each[0:-1] in self.non_finite_verbs["word"].values):
                    non_F = True

            else:
                if each in self.non_finite_verbs["word"].values:
                    non_F = True
                    emphasizer_list.append([[None]])
                    verb_locations.append(
                        {
                            "verb": each,
                            "location": [idx],
                            "original_verb": each,
                        }
                    )

                elif each[-1] in emphasizer_characters and each[:-1] in self.non_finite_verbs["word"].values:
                    non_F = True
                    emphasizer_list.append([[each[-1]]])
                    verb_locations.append(
                        {
                            "verb": each[:-1],
                            "location": [idx],
                            "original_verb": each,
                        }
                    )

            vlen = len(verb_locations)
            vlen -= 1
            # if non_F = true and alreadyFound = false, that means we have to find parent from non_finite
            if non_F or alreadyFound:
                non_finte[vlen] = [non_F, alreadyFound]

            # generating information for every found verbs
        for i, each in enumerate(verb_locations):
            info = []
            tense_person_emp = []
            if non_finte[i][1]:
                info = self.data[self.data["word"] == each["verb"]]
                for eachx in zip(info["tense"], info["person"]):
                    obj = {
                        "tense": eachx[0],
                        "person": eachx[1]
                    }
                    if(obj not in tense_person_emp):
                        tense_person_emp.append(obj)
            else:
                info = self.non_finite_verbs[self.non_finite_verbs["word"]
                                             == each["verb"]]

            verb.append(
                {
                    "Index": each["location"],
                    "original_word": each["original_verb"],
                    "Parent_Verb": info["parent_word"].iloc[0],
                    "Emphasizer": emphasizer_list[i],
                    "TP": tense_person_emp,
                    "Non_Finite": non_finte[i][0],
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

            for i, y in enumerate(keys):
                if len(index) > 1:
                    tokens[y]["Verb"]["Related_Indices"].append(
                        index[(i+1) % 2])
                tokens[y]["Verb"]["Emphasizer"] = x["Emphasizer"][i]
                tokens[y]["Verb"]["TP"] = x["TP"]
                tokens[y]["Verb"]["Parent_Verb"] = x["Parent_Verb"]
                tokens[y]["Verb"]["Non_Finite"] = x["Non_Finite"]
                tokens[y]["Verb"]["Language_Form"] = x["Language_Form"]

        return verb_indexes

    # print(sentence)
    # verb_lemmatizer(sentence)
