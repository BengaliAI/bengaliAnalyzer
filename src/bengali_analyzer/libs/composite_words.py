from indicparser import graphemeParser


class CompositeWordAnalyzer:
    def __init__(self, dictionary_words, prefixes, suffixes, special_suffixes):
        self.grapheme_parser = graphemeParser("bangla")
        self.graphemes = None
        self.dictionary_words = dictionary_words
        self.prefixes = prefixes
        self.suffixes = suffixes
        self.special_suffixes = special_suffixes
        self.substring_set = None

    # Validate prefix
    def validate_prefix(self, word):
        self.graphemes = self.grapheme_parser.process(word)
        for i in range(len(word) + 1):
            substring = word[:i]
            if (
                substring in self.dictionary_words
                and substring not in self.graphemes
                and len(substring) > 1
            ):
                return True
        return False

    # Validate suffix
    def validate_suffix(self, word):
        self.graphemes = self.grapheme_parser.process(word)
        for i in range(len(word)):
            substring = word[-i:]
            if (
                substring in self.dictionary_words
                and substring not in self.graphemes
                and len(substring) > 1
            ):
                return True
        return False

    # Normal dataset based suffix extraction
    def get_general_suffix_extraction(self, word):
        matched_suffixes = []
        for suffix in self.suffixes.keys():
            if suffix in word[len(word) - len(suffix) :]:
                matched_suffixes.append(suffix)
        matched_suffixes.sort(reverse=True)
        for suffix in matched_suffixes:
            word_copy = word[: -len(suffix)]
            try:
                if self.validate_suffix(word_copy):
                    return word_copy, suffix
            except: 
                continue
        return None, None

    # Rule based suffix extraction
    def get_rule_based_suffix_extraction(self, word):
        longest_special_suffix = None

        # `য়` special vowel diacritic based suffix extraction
        vowel_diacritics = {"া", "ি", "ী", "ু", "ূ", "ৃ", "ে", "ৈ", "ো", "ৌ"}
        if (
            word[-1] == "য়"
            and word[-2] in vowel_diacritics
            and self.validate_suffix(word[:-1])
        ):
            return word[:-1], "য়"
        #
        matched_special_suffixes = []
        for special_suffix in self.special_suffixes.keys():
            if special_suffix in word[len(word) - len(special_suffix) :]:
                matched_special_suffixes.append(special_suffix)
            if matched_special_suffixes:
                longest_special_suffix = max(matched_special_suffixes, key=len)
                word_copy = word[: -len(longest_special_suffix)]
                if self.validate_suffix(word_copy):
                    return word_copy, longest_special_suffix
        return None, None

    # Normal dataset based prefix extraction
    def get_prefix_extraction(self, word):
        matched_prefixes = []
        max_length_prefix = max(self.prefixes.keys(), key=len)
        longest_prefix = None

        for prefix in self.prefixes.keys():
            if (
                len(max_length_prefix) < len(word)
                and prefix in word[: -(len(word) - len(prefix))]
            ):
                matched_prefixes.append(prefix)

        if matched_prefixes:
            for prefix in matched_prefixes:
                word_copy = word[len(prefix) :]
                try:
                    if self.validate_prefix(word_copy):
                        return word_copy, prefix
                except:
                    continue
        return None, None

    def get_all_possible_substrings(self, graphemes):
        all_possible_substrings = []
        for i in range(len(graphemes)):
            substring = graphemes[i]
            for j in range(i + 1, len(graphemes)):
                substring += graphemes[j]
                if substring in self.dictionary_words:
                    all_possible_substrings.append(substring)
        return all_possible_substrings

    def powerset(self, s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]

    # Return valid stand-alone words
    def get_constructing_substrings(self, word):
        stand_alone_substrings = []
        self.graphemes = self.grapheme_parser.process(word)
        all_possible_substrings = self.get_all_possible_substrings(self.graphemes)
        linear_subsets = self.powerset(all_possible_substrings)
        for set in linear_subsets:
            string = "".join(set)
            if string == word:
                stand_alone_substrings = set
        return stand_alone_substrings

    def analyze_composite_words(self, tokens, flags):
        for word, value in tokens.items():
            indices = tokens[word]["global_index"]
            if set(indices).isdisjoint(set(flags)):
                self.generate_word_configuration(word, tokens)

    def generate_word_configuration(self, word, tokens):
        self.graphemes = None
        key = word

        special_suffix_flag = False
        word_without_suffix, suffix = self.get_general_suffix_extraction(word)
        
        if suffix is None:
            special_suffix_flag = True
            word_without_suffix, suffix = self.get_rule_based_suffix_extraction(word)
        
        word_without_prefix, prefix = self.get_prefix_extraction(word)
        
        if suffix is not None and prefix is not None:
            word = word[len(prefix) :]
            word = word[: -len(suffix)]
            stand_alone_words = self.get_constructing_substrings(word)
            if stand_alone_words is not None:
                tokens[key]["composite_word"]["stand_alone_words"] = stand_alone_words
                tokens[key]["composite_word"]["suffix"] = suffix
                if special_suffix_flag:
                    if suffix == "য়":
                        tokens[key]["composite_word"]["suffix"] = suffix
                    else:
                        tokens[key]["composite_word"]["suffix"] = self.special_suffixes[
                            suffix
                        ]
                tokens[key]["composite_word"]["prefix"] = prefix
        elif suffix is not None:
            word = word[: -len(suffix)]
            stand_alone_words = self.get_constructing_substrings(word)
            if stand_alone_words is not None:
                tokens[key]["composite_word"]["stand_alone_words"] = stand_alone_words
                tokens[key]["composite_word"]["suffix"] = suffix
                if special_suffix_flag:
                    if suffix == "য়":
                        tokens[key]["composite_word"]["suffix"] = suffix
                    else:
                        tokens[key]["composite_word"]["suffix"] = self.special_suffixes[suffix]
        elif prefix is not None:
            word = word[len(prefix) :]
            stand_alone_words = self.get_constructing_substrings(word)
            if stand_alone_words is not None:
                tokens[key]["composite_word"]["stand_alone_words"] = stand_alone_words
                tokens[key]["composite_word"]["prefix"] = prefix
        else:
            stand_alone_words = self.get_constructing_substrings(word)
            if stand_alone_words is not None:
                tokens[key]["composite_word"]["stand_alone_words"] = stand_alone_words
