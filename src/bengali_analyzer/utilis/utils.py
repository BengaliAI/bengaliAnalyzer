import json
from copy import deepcopy


class Utils:
    def sortFunc(self, word):
        return word["index"]

    def getSortedObjectList(self, res):
        sortedRes = []
        sortedList = []
        for word in res:
            indexes = res[word]["Global_Index"]
            for index in indexes:
                if not isinstance(index, int):
                    sortedRes.append(
                        {"word": word, "index": index[0], "Global_Index": index}
                    )
                else:
                    sortedRes.append(
                        {"word": word, "index": index, "Global_Index": index}
                    )
        sortedRes.sort(key=self.sortFunc)
        for element in sortedRes:
            obj = {}
            word = element["word"]
            global_index = element["Global_Index"]
            obj = deepcopy(res[word])
            obj["Orginal_Global_Index"] = obj["Global_Index"]
            obj["Global_Index"] = [global_index]
            obj["word"] = word
            sortedList.append(obj)
        return sortedList

    def getRelatedWords(self, res, related_index, parent_index):
        for word in res:
            word_obj = res[word]
            indexes = word_obj["Global_Index"]
            nonFinite = False
            if "Verb" in word_obj:
                if "Non_Finite" in word_obj["Verb"]:
                    nonFinite = word_obj["Verb"]["Non_Finite"]
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
            # Numeric
            dataNumeric = data[x]["Numeric"]
            for y in dataNumeric.copy():
                if not dataNumeric[y]:
                    del data[x]["Numeric"][y]
                    ok = 1
            if not dataNumeric:
                del data[x]["Numeric"]

            # Punctuation
            dataPunction = data[x]["Punctuation_Flag"]
            if not dataPunction:
                del data[x]["Punctuation_Flag"]

            # Verb
            dataVerb = data[x]["Verb"]
            for y in dataVerb.copy():
                if not dataVerb[y] or (y == "Emphasizer" and not dataVerb[y][0]):
                    del data[x]["Verb"][y]
                    ok = 1
            if not dataVerb:
                del data[x]["Verb"]

            # Pronoun
            dataPronoun = data[x]["Pronoun"]
            for y in dataPronoun.copy():
                if not dataPronoun[y]:
                    del data[x]["Pronoun"][y]
            if not dataPronoun:
                del data[x]["Pronoun"]

            # Pos
            if not data[x]["PoS"]:
                del data[x]["PoS"]

            # Composite Word
            dataComposite = data[x]["Composite_Word"]
            for y in dataComposite.copy():
                if not dataComposite[y]:
                    del data[x]["Composite_Word"][y]
            if not dataComposite:
                del data[x]["Composite_Word"]

            # Special Entity
            dataSpecial = data[x]["Special_Entity"]
            for y in dataSpecial.copy():
                if not dataSpecial[y]:
                    del data[x]["Special_Entity"][y]
            if not dataSpecial:
                del data[x]["Special_Entity"]
        return data
