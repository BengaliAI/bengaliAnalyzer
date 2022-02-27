class SpecialEntityAnalyzer:
    def __init__(self, entity_list):
        self.entity_list = entity_list

    def flag_special_entity(self, tokens, sentence):
        flags = []
        found_entities = []
        for entity in self.entity_list:
            if entity in sentence:
                found_entities.append(entity)

        found_entities_copy = found_entities.copy()

        for entity in found_entities_copy:
            for entity2 in found_entities_copy:
                if entity in entity2 and len(entity) < len(entity2) and entity in found_entities:
                    found_entities.remove(entity)

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
