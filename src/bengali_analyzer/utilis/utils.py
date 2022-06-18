import json
from copy import deepcopy


class Utils:
    def sortFunc(self, word):
        return word["index"]

    def getSortedObjectList(self, res):
        sortedRes = []
        sortedList = []
        for word in res:
            indexes = res[word]["global_index"]
            for index in indexes:
                if not isinstance(index, int):
                    sortedRes.append(
                        {"word": word, "index": index[0], "global_index": index}
                    )
                else:
                    sortedRes.append(
                        {"word": word, "index": index, "global_index": index}
                    )
        sortedRes.sort(key=self.sortFunc)
        for element in sortedRes:
            obj = {}
            word = element["word"]
            global_index = element["global_index"]
            obj = deepcopy(res[word])
            obj["Orginal_Global_Index"] = obj["global_index"]
            obj["global_index"] = [global_index]
            obj["word"] = word
            sortedList.append(obj)
        return sortedList

    def getRelatedWords(self, res, related_index, parent_index):
        for word in res:
            word_obj = res[word]
            indexes = word_obj["global_index"]
            nonFinite = False
            if "verb" in word_obj:
                if "non_finite" in word_obj["verb"]:
                    nonFinite = word_obj["verb"]["non_finite"]
            for index in indexes:
                if type(index) is list:
                    if (
                        index == related_index
                        and index[0] > parent_index[0]
                        and not nonFinite
                    ):
                        return word

        return -1

    def serializeSets(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return obj

    def updateLog(self, dataDict):
        with open("./fullResponse.json", "w", encoding="utf-8") as f:
            json.dump(
                dataDict, f, ensure_ascii=False, default=self.serializeSets, indent=4
            )

    def fixJSONFormat(self, dataDict):
        dataDict = self.simplifyJson(dataDict)
        datastr = json.dumps(dataDict, default=self.serializeSets, indent=4)
        return json.loads(datastr)

    def simplifyJson(self, data):
        for x in data.copy():
            # numeric
            dataNumeric = data[x]["numeric"]
            for y in dataNumeric.copy():
                if not dataNumeric[y]:
                    del data[x]["numeric"][y]
                    ok = 1
            if not dataNumeric:
                del data[x]["numeric"]

            # Punctuation
            dataPunction = data[x]["punctuation_flag"]
            if not dataPunction:
                del data[x]["punctuation_flag"]

            # verb
            dataVerb = data[x]["verb"]
            for y in dataVerb.copy():
                if not dataVerb[y] or (y == "emphasizer" and not dataVerb[y][0]):
                    del data[x]["verb"][y]
                    ok = 1
            if not dataVerb:
                del data[x]["verb"]

            # pronoun
            dataPronoun = data[x]["pronoun"]
            for y in dataPronoun.copy():
                if not dataPronoun[y]:
                    del data[x]["pronoun"][y]
            if not dataPronoun:
                del data[x]["pronoun"]

            # Pos
            if not data[x]["pos"]:
                del data[x]["pos"]

            # Composite Word
            dataComposite = data[x]["composite_word"]
            for y in dataComposite.copy():
                if not dataComposite[y]:
                    del data[x]["composite_word"][y]
            if not dataComposite:
                del data[x]["composite_word"]

            # Special Entity
            dataSpecial = data[x]["special_entity"]
            for y in dataSpecial.copy():
                if not dataSpecial[y]:
                    del data[x]["special_entity"][y]
            if not dataSpecial:
                del data[x]["special_entity"]
        return data
