class SpecialEntityAnalyzer:
    def __init__(self, suffixes,entity_list):
        self.suffixes = suffixes
        self.entity_list = entity_list

    #data = sorted(data, key = lambda a: a[0] if type(a) is tuple else a)
    
    def flag_special_entity(self, tokens, sentence):
        flags = []
        found_entities = []
        for entity in self.entity_list:
            if entity in sentence:
                found_entities.append(entity)

        print(found_entities, "found entry initial")

        found_entities_copy = found_entities.copy()

        for entity in found_entities_copy:
            for entity2 in found_entities_copy:
                if entity in entity2 and len(entity) < len(entity2) and entity in found_entities:
                    found_entities.remove(entity)

        print(found_entities, "found entry after removing instersecting strings")

        punctuations = {
            " ",
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
        }

        for entity in found_entities:
            index = 1
            while (entity[-index] not in punctuation):
                index += 1
            last_token = entity[-index:]    
            if not tokens[last_token]:
                for token in tokens.keys():
                    if last_token in token:
                        probable_suffix = token[:-len(last_token)]     

        string_buffer = ""

        end_index = 0
        start_index = 0
        for index in range(len(sentence)):
            if sentence[index] not in punctuations:
                string_buffer += sentence[index]
                end_index = index
                if index == len(sentence) - 1:
                    if string_buffer != "":
                        global_index = (start_index, end_index)
                        if string_buffer not in tokens.keys():
                            tokens[string_buffer] = copy.deepcopy(token)
                        tokens[string_buffer]["Punctuation_Flag"] = False
                        tokens[string_buffer]["Global_Index"].append(
                            global_index)
            else:
                if string_buffer != "":
                    string_buffer = normalize_token(string_buffer)
                    global_index = (start_index, end_index)
                    if string_buffer not in tokens.keys():
                        tokens[string_buffer] = copy.deepcopy(token)
                    tokens[string_buffer]["Punctuation_Flag"] = False
                    tokens[string_buffer]["Global_Index"].append(global_index)
                    string_buffer = ""

                punctuation_flags.append(index)
                start_index = index + 1
                punctuation = sentence[index]

                if punctuation not in tokens.keys():
                    tokens[punctuation] = copy.deepcopy(token)
                tokens[punctuation]["Punctuation_Flag"] = True
                tokens[punctuation]["Global_Index"].append(index)



        related_index = {}
        flagged_token = set()
        for entity in found_entities:
            indices = []
            for token in tokens.keys():
                if token in entity:
                    flagged_token.add(token)
                    indices.extend(tokens[token]["Global_Index"])
                    flags.extend(tokens[token]["Global_Index"])
            related_index[entity] = indices

        for entity in related_index.keys():
            for indices in related_index[entity]:
                for token in flagged_token:
                    tokens[token]["Special_Entity"]["Related_Indices"].append(indices)
        return flags
