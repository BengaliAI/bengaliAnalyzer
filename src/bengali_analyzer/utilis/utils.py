import json

class Utils:
    def sortFunc(self, word):
        return word["index"]

    def getRelatedWords(self, res,related_index):
        for word in res:
            word_obj = res[word]
            
            indexes = word_obj['Global_Index']
            if type(indexes[0]) is list:
                if indexes[0][0] == related_index:
                    return word
        return -1

    def serializeSets(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return obj

    def updateLog(self, dataDict):
        with open("./fullResponse.json", "w", encoding="utf-8") as f:
            json.dump(dataDict, f, ensure_ascii=False, default=self.serializeSets, indent=4)

    def fixJSONFormat(self, dataDict):
        dataDict = self.simplifyJson(dataDict)
        datastr = json.dumps(dataDict, default=self.serializeSets, indent=4)
        return json.loads(datastr)

    def simplifyJson(self, data):
        for x in data.copy():
            # Numeric
            dataNumeric = data[x]["Numeric"]
            for y in dataNumeric.copy():
                if(not dataNumeric[y]):
                    del(data[x]["Numeric"][y])
                    ok = 1
            if(not dataNumeric):
                del(data[x]["Numeric"])
            
            # Punctuation
            dataPunction = data[x]["Punctuation_Flag"]
            if(not dataPunction):
                del(data[x]["Punctuation_Flag"])
            
            # Verb
            dataVerb = data[x]["Verb"]
            for y in dataVerb.copy():
                if(not dataVerb[y] or (y=='Emphasizer' and not dataVerb[y][0])):
                    del(data[x]["Verb"][y])
                    ok = 1
            if(not dataVerb):
                del(data[x]["Verb"])

            # Pronoun
            dataPronoun = data[x]["Pronoun"]
            for y in dataPronoun.copy():
                if(not dataPronoun[y]):
                    del(data[x]["Pronoun"][y])
            if(not dataPronoun):
                del(data[x]["Pronoun"])

            # Pos
            if(not data[x]["PoS"]):
                del(data[x]["PoS"])

            # Composite Word
            dataComposite = data[x]["Composite_Word"]
            for y in dataComposite.copy():
                if(not dataComposite[y]):
                    del(data[x]["Composite_Word"][y])
            if(not dataComposite):
                del(data[x]["Composite_Word"])

            # Special Entity
            dataSpecial = data[x]["Special_Entity"]
            for y in dataSpecial.copy():
                if(not dataSpecial[y]):
                    del(data[x]["Special_Entity"][y])
            if(not dataSpecial):
                del(data[x]["Special_Entity"])
        return data

