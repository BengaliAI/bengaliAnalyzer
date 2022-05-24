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
        if self.graphemes is None:
            self.graphemes = self.grapheme_parser.process(word)
        for i in range(len(word) + 1):
            substring = word[:i]
            if substring in self.dictionary_words and substring not in self.graphemes and len(substring) > 1:
                return True
        self.graphemes = None
        return False

    # Validate suffix
    def validate_suffix(self, word):
        if self.graphemes is None:
            self.graphemes = self.grapheme_parser.process(word)
        for i in range(len(word)):
            substring = word[-i:]
            if substring in self.dictionary_words and substring not in self.graphemes and len(substring) > 1:
                return True
        self.graphemes = None
        return False

    # Create all the combinations of substrings
    def get_powerset(self, word):
        if self.graphemes is None:
            self.graphemes = self.grapheme_parser.process(word)

        length = len(self.substring_set)
        return {
            frozenset({e for e, b in zip(self.substring_set, f'{i:{length}b}') if b == '1'})
            for i in range(2 ** length)}

    # Get all valid substrings of a word
    def get_all_possible_substrings(self, word):
        if self.graphemes is None:
            self.graphemes = self.grapheme_parser.process(word)
        all_possible_substrings = set()
        for index, grapheme1 in enumerate(self.graphemes):
            substring = grapheme1
            for index2, grapheme2 in enumerate(self.graphemes):
                if index < index2:
                    substring += grapheme2
                    all_possible_substrings.add(substring)
        copy = all_possible_substrings.copy()
        for key in copy:
            if key not in self.dictionary_words.keys():
                all_possible_substrings.discard(key)
        return all_possible_substrings

    # Return valid stand-alone words
    def get_constructing_substrings(self, word):
        self.substring_set = self.get_all_possible_substrings(word)
        valid_substrings = set()
        all_possible_subset = self.get_powerset(word)
        all_possible_subset.discard(frozenset())
        for subset in all_possible_subset:
            constructed_word = ''
            for substring in subset:
                constructed_word += substring
            if constructed_word == word:
                valid_substrings.add(subset)
        stand_alone_substrings = []
        if valid_substrings:
            for elements in valid_substrings:
                for element in elements:
                    stand_alone_substrings.append(element)
        else:
            substring_set_copy = self.substring_set.copy()
            for element in substring_set_copy:
                for element2 in substring_set_copy:
                    if len(element) < len(element2) and element in element2:
                        self.substring_set.discard(element)
            stand_alone_substrings = list(self.substring_set)
        return stand_alone_substrings

    def analyze_composite_words(self, tokens, flags):
        for word, value in tokens.items():
            indices = tokens[word]['Global_Index']
            if set(indices).isdisjoint(set(flags)):
                self.generate_word_configuration(word, tokens)

    def generate_word_configuration(self, word, tokens):
        self.graphemes = None
        key = word
        matched_suffixes = []
        matched_prefixes = []
        matched_special_suffixes = []
        could_be_special_suffix = True

        for suffix in self.suffixes.keys():
            if suffix in word[len(word) - len(suffix):]:
                matched_suffixes.append(suffix)
        if matched_suffixes:
            longest_suffix = max(matched_suffixes, key=len)
            word_copy = word[:-len(longest_suffix)]
            if self.validate_suffix(word_copy):
                tokens[key]['Composite_Word']['Stand_Alone_Words'].add(word_copy)
                tokens[key]['Composite_Word']["Suffix"] = longest_suffix
                word = word_copy
                could_be_special_suffix = False

        if could_be_special_suffix:
            for special_suffix in self.special_suffixes.keys():
                if special_suffix in word[len(word) - len(special_suffix):]:
                    matched_special_suffixes.append(special_suffix)
            if matched_special_suffixes:
                longest_special_suffix = max(matched_special_suffixes, key=len)
                word_copy = word[:- len(longest_special_suffix)]
                if self.validate_suffix(word_copy):
                    tokens[key]['Composite_Word']['Suffix'] = self.special_suffixes[longest_special_suffix]
                    tokens[key]['Composite_Word']['Stand_Alone_Words'].add(word_copy)
                    word = word_copy

        max_length_prefix = max(self.prefixes.keys(), key=len)
        for prefix in self.prefixes.keys():
            if len(max_length_prefix) < len(word) and prefix in word[:-(len(word) - len(prefix))]:
                matched_prefixes.append(prefix)
        if matched_prefixes:
            longest_prefix = max(matched_prefixes, key=len)
            word_copy = word[len(longest_prefix):]
            if self.validate_prefix(word_copy):
                tokens[key]['Composite_Word']['Stand_Alone_Words'].add(word_copy)
                tokens[key]['Composite_Word']["Prefix"] = longest_prefix
                word = word_copy

        stand_alone_words = self.get_constructing_substrings(word)
        tokens[key]['Composite_Word']["Stand_Alone_Words"].update(stand_alone_words)
        if not stand_alone_words:
            tokens[key]['Composite_Word']['Stand_Alone_Words'].add(word)
