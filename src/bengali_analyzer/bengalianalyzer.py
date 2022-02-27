import copy
import os
import string
import pandas


# from libs import verbs
# from libs import composite_words
# from libs import non_verbs
# from libs import numerics
# from libs import special_entity

from .libs import verbs
from .libs import composite_words
from .libs import non_verbs
from .libs import numerics
from .libs import special_entity


global verb_data, verb_data_1, verb_data_2, not_to_be_broken, prefixes, suffixes, special_cases, non_verb_words, special_suffixes


def remove_symbols(string_line):
    clean_string = string_line
    symbols = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯', '_', '-', '(', ')', ' ', '.', ';', '[', ']', "'",
               '&', ".", ",", ";", ":", "!", "?", "\"", "'", "`", "~", "^", "*", "(", ")", "[", "]", "{", "}",
               "।"]  # Add more if necessary # ? -> '’'
    symbols += string.ascii_letters
    for symbol in symbols:
        if symbol in clean_string:
            clean_string = clean_string.replace(symbol, "")
    return clean_string


def prepare_special_suffixes(datafile):
    data = pandas.read_csv(datafile, encoding="utf8", header=None, names=["keys", "values"])
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    dictionary = {}
    for idx in range(len(data)):
        _key = data.iloc[idx, 0]
        _value = data.iloc[idx, 1]
        dictionary[_key] = _value
    return dictionary


def prepare_non_verb_data(data_file):
    data = pandas.read_csv(data_file, encoding="utf8", header=None, names=["keys", "values"])
    data = data.drop_duplicates()
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    data_dict = {}

    for idx in range(len(data)):
        _key = remove_symbols(data.iloc[idx, 0])
        _value = remove_symbols(data.iloc[idx, 1])
        data_dict[_key] = _value

    return data_dict


def prepare_verb_data(data):
    data = pandas.read_csv(data)
    count = []
    for each in data['word'].values:
        count.append(len(each.split(' ')))
    data['count'] = count
    data2 = data[data['count'] == 2]
    data1 = data[data['count'] == 1]
    return data, data1, data2


def clean_generated_dictionary(dictionary):
    clean_dictionary = dictionary.copy()
    for key in dictionary.keys():
        if key == '' or key[-1] == '্':
            clean_dictionary.pop(key)

    for key in suffixes.keys():
        if key in clean_dictionary.keys():
            clean_dictionary.pop(key)

    for key in prefixes.keys():
        if key in dictionary.keys():
            if key in clean_dictionary.keys():
                clean_dictionary.pop(key)

    return clean_dictionary


def generate_special_entity(file):
    a_file = open(file)

    file_contents = a_file.read()
    dictionary = file_contents.splitlines()
    a_file.close()
    return dictionary


def generate_dictionary(file):
    dictionary = {}
    with open(file, "r", encoding="utf8") as raw_file:
        lines = raw_file.readlines()
        for line in lines:
            if ' - ' or ' ' or ',' or '.' in line:
                noisy_separators = [' - ', ' ', ' . ']
                for noisy_separator in noisy_separators:
                    line = line.replace(noisy_separator, ',')
                line = line.split(',')
                for word in line:
                    word = remove_symbols(word).strip()
                    if word != '' and word[-1] != '্':
                        dictionary[word] = []
            else:
                line = remove_symbols(line)
                if line != '' and line[-1] != '্':
                    dictionary[remove_symbols(line.strip())] = []
    return dictionary


# Required to preload datasets
def load_data():
    global verb_data, verb_data_1, verb_data_2, not_to_be_broken, prefixes, suffixes, special_cases, non_verb_words, special_suffixes
    path = os.path.dirname(os.path.abspath(__file__))
    asset_directory = os.path.join(path, 'assets')

    # Generate verb data
    verb_data = os.path.join(asset_directory, "verbs.csv")
    verb_data, verb_data_1, verb_data_2 = prepare_verb_data(verb_data)

    # Generate non-verb data
    non_verb_words = os.path.join(asset_directory, 'non_verbs.csv')
    non_verb_words = prepare_non_verb_data(non_verb_words)

    # Generate other data,
    not_to_be_broken_file = os.path.join(asset_directory, 'not_to_be_broken.txt')
    suffix_file = os.path.join(asset_directory, 'suffixes.csv')
    prefix_file = os.path.join(asset_directory, 'prefixes.csv')
    special_suffixes_file = os.path.join(asset_directory, 'special_suffixes.csv')

    special_suffixes = prepare_special_suffixes(special_suffixes_file)
    not_to_be_broken = generate_special_entity(not_to_be_broken_file)
    suffixes = generate_dictionary(suffix_file)
    prefixes = generate_dictionary(prefix_file)

    non_verb_words = clean_generated_dictionary(non_verb_words)


class BengaliAnalyzer:
    def __init__(self):
        load_data()
        self.numeric_analyzer = numerics.NumericAnalyzer()
        self.verbs_analyzer = verbs.VerbAnalyzer(verb_data, verb_data_1, verb_data_2)
        self.non_verbs_analyzer = non_verbs.NonVerbAnalyzer(non_verb_words)
        self.composite_words_analyzer = composite_words.CompositeWordAnalyzer(non_verb_words, prefixes, suffixes,
                                                                              special_suffixes)
        self.special_entity_analyzer = special_entity.SpecialEntityAnalyzer(not_to_be_broken)

    @staticmethod
    def tokenize_sentence(sentence):
        token = {
            "Global_Index": [],
            "Punctuation_Flag": True,
            "Numeric":
                {
                    "Digit": None,
                    "Literal": None,
                    "Weight": None,
                    "Suffix": []
                },
            "Verb":
                {
                    "Parent_Verb": None,
                    "Tense_Person_Emphasis": None,
                    "Form": None,
                    "Related_Indices": [],
                },
            "Non_Verb": None,
            "Composite_Word":
                {
                    "Suffix": None,
                    "Prefix": None,
                    "Stand_Alone_Words": set(),
                },
            "Special_Entity":
                {
                    "Definition": None,
                    "Related_Indices": []
                }
        }
        tokens = {}
        punctuation_flags = []
        punctuations = {" ", ".", ",", ";", ":", "!", "?", "\"", "'", "`", "~", "^", "*", "(", ")", "[", "]", "{", "}",
                        "।"}

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
                        tokens[string_buffer] = copy.deepcopy(token)
                        tokens[string_buffer]["Punctuation_Flag"] = False
                        tokens[string_buffer]["Global_Index"].append(global_index)
            else:
                if string_buffer != "":
                    global_index = (start_index, end_index)
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

        return tokens, punctuation_flags

    def analyze_sentence(self, sentence):
        flags = []

        tokens, punctuation_flags = self.tokenize_sentence(sentence)
        flags.extend(punctuation_flags)

        numeric_flags = self.numeric_analyzer.get_numerics(tokens)
        flags.extend(numeric_flags)

        special_entity_flags = self.special_entity_analyzer.flag_special_entity(tokens, sentence)
        flags.extend(special_entity_flags)

        verb_flags = self.verbs_analyzer.get_verbs(tokens, sentence)
        flags.extend(verb_flags)

        non_verb_flags = self.non_verbs_analyzer.get_non_verbs(tokens)
        flags.extend(non_verb_flags)

        self.composite_words_analyzer.analyze_composite_words(tokens, flags)

        return tokens
