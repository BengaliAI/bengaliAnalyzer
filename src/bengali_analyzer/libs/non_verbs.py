class NonVerbAnalyzer:
    def __init__(self, dictionary_words):
        self.dictionary_words = dictionary_words

    def get_non_verbs(self, tokens):
        new_flags = []
        for key, value in tokens.items():
            if key in self.dictionary_words.keys():
                new_flags.extend(tokens[key]["global_index"])
                tokens[key]["pos"] = self.dictionary_words[key]
        return new_flags
