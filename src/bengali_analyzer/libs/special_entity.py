class SpecialEntityAnalyzer:
    def __init__(self, suffixes, entity_list):
        self.suffixes = suffixes
        self.entity_list = entity_list

    def validate_suffix(self, tokens, entity):
        entity = entity.strip()
        token_index = None
        token_candidate = None
        for token in tokens.keys():
            if len(token) > len(entity) and token[len(entity) :] in self.suffixes:
                tokens[token]["special_entity"]["suffix"] = token[len(entity) :]
                token_index = tokens[token]["global_index"]
                token_candidate = token
                break
        return token_candidate, token_index

    def tokenize_special_entity(self, tokens, entity):

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

        related_indices = []

        releated_tokens = set()

        # The spacing indice
        space_index = set()
        for x in range(len(entity)):
            if entity[x] == " ":
                space_index.add(x)

        punctuation_list = [p for p in punctuations if p in entity and p != " "]
        for punctuation in punctuation_list:
            related_indices.add(tokens[punctuation]["global_index"])
            releated_tokens.add(punctuation)

        for p in punctuation_list:
            entity = entity.replace(p, "")
        words = entity.split(" ")
        for word in words:
            if word in tokens.keys():
                related_indices.extend(tokens[word]["global_index"])
                releated_tokens.add(word)
            else:
                token, index = self.validate_suffix(tokens, word)
                if token is not None:
                    related_indices.extend(index)
                    releated_tokens.add(token)

        related_indices = sorted(
            related_indices, key=lambda a: a[0] if type(a) is tuple else a
        )
        for token in releated_tokens:
            tokens[token]["special_entity"]["related_indices"] = related_indices
            tokens[token]["special_entity"]["space_indices"] = space_index
        return related_indices

    # A slave function to find special entities in a sentence
    def find_special_entity(
        self,
        sentence,
    ):
        found_entities = []
        for entity in self.entity_list:
            if entity in sentence:
                found_entities.append(entity)

        found_entities_copy = found_entities.copy()

        for entity in found_entities_copy:
            for entity2 in found_entities_copy:
                if (
                    entity in entity2
                    and len(entity) < len(entity2)
                    and entity in found_entities
                ):
                    found_entities.remove(entity)
        return found_entities

    def flag_special_entity(self, tokens, sentence):
        found_entities = self.find_special_entity(sentence)
        flags = []
        for entity in found_entities:
            flags.extend(self.tokenize_special_entity(tokens, entity))

        return flags
