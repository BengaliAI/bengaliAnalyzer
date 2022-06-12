import copy
import os
import string
import pandas
import json
import csv
from .normalizer import normalize_assets
from bnunicodenormalizer import Normalizer


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
from .libs import pronouns
from .utilis import utils

global verb_data, verb_data_1, verb_data_2, not_to_be_broken, prefixes, suffixes, special_cases, non_verb_words, special_suffixes, pronoun_data, numeric_digit, numeric_literals, numeric_weights, numeric_suffixes, numeric_prefixes, numeric_months, numeric_special_cases, numeric_days


def normalize_token(word):
    bn_normalizer = Normalizer()
    normalized_token = bn_normalizer(word)
    # return word
    return normalized_token["normalized"]


def remove_symbols(string_line):
    clean_string = string_line
    symbols = [
        "০",
        "১",
        "২",
        "৩",
        "৪",
        "৫",
        "৬",
        "৭",
        "৮",
        "৯",
        "_",
        "-",
        "(",
        ")",
        " ",
        ".",
        ";",
        "[",
        "]",
        "'",
        "&",
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
    ]  # Add more if necessary # ? -> '’'
    symbols += string.ascii_letters
    for symbol in symbols:
        if symbol in clean_string:
            clean_string = clean_string.replace(symbol, "")
    return clean_string


def prepare_special_suffixes(datafile):
    data = pandas.read_csv(
        datafile, encoding="utf8", header=None, names=["keys", "values"]
    )
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    dictionary = {}
    for idx in range(len(data)):
        _key = data.iloc[idx, 0]
        _value = data.iloc[idx, 1]
        dictionary[_key] = _value
    return dictionary


def prepare_non_verb_data(data_file):
    data = pandas.read_csv(
        data_file, encoding="utf8", header=None, names=["keys", "values"]
    )
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    data_dict = {}

    for idx in range(len(data)):
        _key = remove_symbols(data.iloc[idx, 0])
        _value = remove_symbols(data.iloc[idx, 1])
        if data_dict.get(_key):
            data_dict[_key].append(_value)
        else:
            data_dict[_key] = [_value]
    return data_dict


def prepare_word_list_data(data_file):
    data = pandas.read_csv(
        data_file,
        encoding="utf8",
        header=None,
    )
    data_dict = {}
    for idx in range(len(data)):
        _key = data.iloc[idx, 0]
        _value = data.iloc[idx, 1:].values

        for each in _value:
            if each == each:
                if data_dict.get(_key):
                    if not each in data_dict[_key]:
                        data_dict[_key].append(each)
                else:
                    data_dict[_key] = [each]
    return data_dict


def prepare_pronoun_data(data_file):
    data = pandas.read_csv(data_file, encoding="utf8", delimiter=",")
    data_dict = {}
    with open(data_file, "r", encoding="utf8") as csvfile:
        datareader = csv.reader(csvfile)
        datareader = list(datareader)
        for row in datareader[1:]:
            temp_dict = {}
            i = 1
            for col in row[1:]:
                if not col:
                    temp_dict[datareader[0][i]] = None
                else:
                    temp_dict[datareader[0][i]] = col
                i += 1
            data_dict[row[0]] = temp_dict
    return data_dict


def prepare_numeric_data(file):
    with open(file, "r", encoding="utf8") as f:
        data = json.load(f)
    numeric_digit = data["digits"]
    numeric_literals = data["literals"]
    numeric_weights = data["weights"]
    numeric_suffixes = data["suffixes"]
    numeric_prefixes = data["prefixes"]
    numeric_special_cases = data["special_cases"]
    numeric_months = data["months"]
    numeric_days = data["days"]
    return (
        numeric_digit,
        numeric_literals,
        numeric_weights,
        numeric_suffixes,
        numeric_prefixes,
        numeric_months,
        numeric_special_cases,
        numeric_days,
    )


def prepare_verb_data(allVerbData, nonFiniteVerbData):
    data = pandas.read_csv(allVerbData)
    count = []
    for each in data["word"].values:
        count.append(len(each.split(" ")))
    data["count"] = count
    data2 = data[data["count"] == 2]
    data1 = data[data["count"] == 1]
    nonFiniteVerbs = pandas.read_csv(nonFiniteVerbData)
    return data, data1, data2, nonFiniteVerbs


def clean_generated_dictionary(dictionary):
    clean_dictionary = dictionary.copy()
    for key in dictionary.keys():
        if key == "" or key[-1] == "্":
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
    a_file = open(file, encoding="utf8")

    file_contents = a_file.read()
    dictionary = file_contents.splitlines()
    a_file.close()
    return dictionary


def generate_dictionary(file):
    dictionary = {}
    with open(file, "r", encoding="utf8") as raw_file:
        lines = raw_file.readlines()
        for line in lines:
            if " - " or " " or "," or "." in line:
                noisy_separators = [" - ", " ", " . "]
                for noisy_separator in noisy_separators:
                    line = line.replace(noisy_separator, ",")
                line = line.split(",")
                for word in line:
                    word = remove_symbols(word).strip()
                    if word != "" and word[-1] != "্":
                        dictionary[word] = []
            else:
                line = remove_symbols(line)
                if line != "" and line[-1] != "্":
                    dictionary[remove_symbols(line.strip())] = []
    return dictionary


# Required to preload datasets
def load_data():
    global verb_data, verb_data_1, verb_data_2, non_finite_verbs, not_to_be_broken, prefixes, suffixes, special_cases, non_verb_words, special_suffixes, pronoun_data, numeric_digit, numeric_literals, numeric_weights, numeric_suffixes, numeric_prefixes, numeric_months, numeric_special_cases, numeric_days
    path = os.path.dirname(os.path.abspath(__file__))
    asset_directory = os.path.join(path, "assets")

    # Generate numeric data
    numeric_data = os.path.join(asset_directory, "numerics.json")
    (
        numeric_digit,
        numeric_literals,
        numeric_weights,
        numeric_suffixes,
        numeric_prefixes,
        numeric_months,
        numeric_special_cases,
        numeric_days,
    ) = prepare_numeric_data(numeric_data)

    # Generate verb data
    verb_data = os.path.join(asset_directory, "verbs.csv")
    nonFiniteVerb_data = os.path.join(asset_directory, "banglaNonFiniteVerbs.csv")
    verb_data, verb_data_1, verb_data_2, non_finite_verbs = prepare_verb_data(
        verb_data, nonFiniteVerb_data
    )

    # Generate non-verb data
    # non_verb_words = os.path.join(asset_directory, "non_verbs.csv")
    # non_verb_words = prepare_non_verb_data(non_verb_words)

    # Generate word-list data
    big_word_list = os.path.join(asset_directory, "wordListPoS.csv")
    non_verb_words = prepare_word_list_data(big_word_list)

    # Genereate pronoun-data
    pronoun_data = os.path.join(asset_directory, "pronouns.csv")
    pronoun_data = prepare_pronoun_data(pronoun_data)

    # Generate other data,
    not_to_be_broken_file = os.path.join(asset_directory, "not_to_be_broken.txt")
    suffix_file = os.path.join(asset_directory, "suffixes.csv")
    prefix_file = os.path.join(asset_directory, "prefixes.csv")
    special_suffixes_file = os.path.join(asset_directory, "special_suffixes.csv")

    special_suffixes = prepare_special_suffixes(special_suffixes_file)
    not_to_be_broken = generate_special_entity(not_to_be_broken_file)
    suffixes = generate_dictionary(suffix_file)
    prefixes = generate_dictionary(prefix_file)

    # non_verb_words = clean_generated_dictionary(non_verb_words)


class BengaliAnalyzer:
    def __init__(self):
        # Normalizing the assets
        IGNORE_FILES = []
        ASSET_DIR = os.path.dirname(os.path.abspath(__file__)) + "/assets/"
        normalize_assets.normalize(file_dir=ASSET_DIR, ignore_files=IGNORE_FILES)

        load_data()

        self.numeric_analyzer = numerics.NumericAnalyzer(
            numeric_digit,
            numeric_literals,
            numeric_weights,
            numeric_suffixes,
            numeric_prefixes,
            numeric_months,
            numeric_special_cases,
            numeric_days,
        )
        self.verbs_analyzer = verbs.VerbAnalyzer(
            verb_data, verb_data_1, verb_data_2, non_finite_verbs
        )
        self.non_verbs_analyzer = non_verbs.NonVerbAnalyzer(non_verb_words)
        self.pronoun_analyzer = pronouns.PronounAnalyzer(pronoun_data)
        self.composite_words_analyzer = composite_words.CompositeWordAnalyzer(
            non_verb_words, prefixes, suffixes, special_suffixes
        )
        self.special_entity_analyzer = special_entity.SpecialEntityAnalyzer(
            suffixes, not_to_be_broken
        )
        self.utils = utils.Utils()

    @staticmethod
    def tokenize_sentence(sentence):
        token = {
            "Global_Index": [],
            "Punctuation_Flag": True,
            "Numeric": {
                "Digit": None, 
                "Literal": None, 
                "Weight": None, 
                "Suffix": []
            },
            "Verb": {
                "Parent_Verb": None,
                "Emphasizer": None,
                "TP": None,
                "Non_Finite": False,
                "Form": None,
                "Related_Indices": [],
            },
            "Pronoun": {
                "Pronoun Tag": None,
                "Number Tag": None,
                "Honorificity": None,
                "Case": None,
                "Proximity": None,
                "Encoding": None,
            },
            "PoS": None,
            "Composite_Word": {
                "Suffix": None,
                "Prefix": None,
                "Stand_Alone_Words": set(),
            },
            "Special_Entity": {
                "Definition": None,
                "Related_Indices": [],
                "SpaceIndices": set(),
                "Suffix": None,
            },
        }
        tokens = {}
        punctuation_flags = []

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
                        tokens[string_buffer]["Global_Index"].append(global_index)
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
        if " " in tokens:
            tokens.pop(" ")
        return tokens, punctuation_flags

    def analyze_sentence(self, sentence):

        flags = []

        tokens, punctuation_flags = self.tokenize_sentence(sentence)
        flags.extend(punctuation_flags)

        numeric_flags = self.numeric_analyzer.get_numerics(tokens)
        flags.extend(numeric_flags)
        special_entity_flags = self.special_entity_analyzer.flag_special_entity(
            tokens, sentence
        )
        flags.extend(special_entity_flags)
        verb_flags = self.verbs_analyzer.get_verbs(tokens, sentence)
        flags.extend(verb_flags)

        pronoun_flags = self.pronoun_analyzer.get_pronouns(tokens)
        flags.extend(pronoun_flags)

        non_verb_flags = self.non_verbs_analyzer.get_non_verbs(tokens)
        flags.extend(non_verb_flags)

        self.composite_words_analyzer.analyze_composite_words(tokens, flags)
        self.utils.updateLog(tokens)
        simplifiedJson = self.utils.fixJSONFormat(tokens)
        return simplifiedJson

    def analyze_pos(self, sentence):
        bangla_pos_to_english_pos = {
            "বিশেষণ": "Adjective",
            "বিশেষ্য": "Noun",
            "সর্বনাম": "Pronoun",
            "অব্যয়": "Adjective",
            "ক্রিয়া": "Verb",
            "ক্রিয়াবিশেষণ": "Adverb",
            "ক্রিয়াবিশেষ্য": "Adverb",
            "obboy": "Adjective",
            "kriya": "ক্রিয়া",
            "bisheshon": "বিশেষণ"
        }

        res = self.analyze_sentence(sentence)

        word_objects = []
        pos_list = []
        for word in res:
            body = res[word]
            pos = ["undefined"]

            if "Verb" in body:
                pos = []
                if "PoS" in body:
                    for p in body["PoS"]:
                        pos.append(bangla_pos_to_english_pos[p])

                if "TP" in body["Verb"]:
                    pos.append("Finite_Verb")

                if "Non_Finite" in body["Verb"] and body["Verb"]["Non_Finite"] == True:
                    pos.append("Non-Finite_Verb")

            elif "Pronoun" in body:
                pos = ["Pronoun"]
                for p in body["PoS"]:
                        pos.append(bangla_pos_to_english_pos[p])

            elif "Punctuation_Flag" in body and body["Punctuation_Flag"] == True:
                pos = ["Punctuation"]

            elif "PoS" in body:
                t = []
                for p in body["PoS"]:
                    t.append(bangla_pos_to_english_pos[p])
                pos = t

            indexes = body["Global_Index"]

            for index in indexes:
                if type(index) is list:
                    word_objects.append({"pos": pos, "index": index[0]})
                else:
                    word_objects.append({"pos": pos, "index": index})

        word_objects.sort(key=self.utils.sortFunc)

        for entry in word_objects:
            pos_list.append(entry["pos"])

        return pos_list

    def lemmatize_sentence(self, sentence):
        word_objects = []
        word_list = []
        covered_by_related_indexes = []

        res = self.analyze_sentence(sentence)
        for word in res:
            word_obj = res[word]
            indexes = word_obj["Global_Index"]

            for global_index in indexes:
                words = []
                if global_index not in covered_by_related_indexes:
                    if "Verb" in word_obj:
                        full_word = word
                        useOriginalWord = False

                        for related_index in word_obj["Verb"]["Related_Indices"]:
                            if (
                                related_index not in indexes
                                and related_index not in covered_by_related_indexes
                            ):
                                relatedWord = self.utils.getRelatedWords(
                                    res, related_index
                                )
                                if relatedWord != -1:
                                    covered_by_related_indexes.append(related_index)
                                    full_word = full_word + " " + relatedWord
                                    useOriginalWord = True
                                    break

                        if useOriginalWord:
                            words.append(full_word)
                        else:
                            words.append(word_obj["Verb"]["Parent_Verb"])
                            if "Emphasizer" in word_obj["Verb"]:
                                for emphasizer in word_obj["Verb"]["Emphasizer"]:
                                    words.append(emphasizer)

                    elif "Composite_Word" in word_obj:
                        if "Prefix" in word_obj["Composite_Word"]:
                            words.append(word_obj["Composite_Word"]["Prefix"])

                        if "Stand_Alone_Words" in word_obj["Composite_Word"]:
                            words.append(
                                word_obj["Composite_Word"]["Stand_Alone_Words"]
                            )

                        if "Suffix" in word_obj["Composite_Word"]:
                            words.append(word_obj["Composite_Word"]["Suffix"])

                    else:
                        words.append(word)

                    covered_by_related_indexes.append(global_index)

                    if type(global_index) is list:
                        word_objects.append({"word": words, "index": global_index[0]})
                    else:
                        word_objects.append({"word": words, "index": global_index})

        word_objects.sort(key=self.utils.sortFunc)

        for word_object in word_objects:
            word_list.append(word_object["word"])
        return word_list
