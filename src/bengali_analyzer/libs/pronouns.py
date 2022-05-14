class PronounAnalyzer:
    def __init__(self, pronoun_dict):
        self.pronoun_words = pronoun_dict

    def get_pronouns(self, tokens):
        new_flags = []
        for key, value in tokens.items():
            if key in self.pronoun_words.keys():
                new_flags.extend(tokens[key]["Global_Index"])
                tokens[key]["Pronoun"] = self.pronoun_words[key]
        return new_flags
