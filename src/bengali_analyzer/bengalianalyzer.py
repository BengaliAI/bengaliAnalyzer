import copy
import os
import string
import pandas
import json
import csv

from bnunicodenormalizer import Normalizer


# from libs import verbs
# from libs import composite_words
# from libs import non_verbs
# from libs import numerics
# from libs import special_entity

from .normalizer import normalize_assets
from .libs import verbs
from .libs import composite_words
from .libs import non_verbs
from .libs import numerics
from .libs import special_entity
from .libs import pronouns
from .utilis import utils

global verb_data, verb_data_1, verb_data_2, not_to_be_broken, prefixes, suffixes, special_cases, non_verb_words, special_suffixes, pronoun_data, numeric_digit, numeric_literals, numeric_weights, numeric_suffixes, numeric_prefixes, numeric_months, numeric_special_cases, numeric_days


def normalize_token(word):
    bn_normalizer = Normalizer(allow_english=True)
    normalized_token = bn_normalizer(word)
    # return word
    return normalized_token["normalized"]


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
                    word = word.strip()
                    if word != "" and word[-1] != "্":
                        dictionary[word] = []
            else:
                if line != "" and line[-1] != "্":
                    dictionary[(line.strip())] = []
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
        IGNORE_FILES = ["prefixes.csv", "suffixes.csv", "special_suffixes.csv"]
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        ASSET_DIR = os.path.join(THIS_DIR, "assets" + os.sep)

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
            "global_index": [],
            "punctuation_flag": True,
            "numeric": {"digit": None, "literal": None, "weight": None, "suffix": []},
            "verb": {
                "parent_verb": [],
                "emphasizer": None,
                "tp": None,
                "non_finite": False,
                "contentative_verb": False,
                "form": None,
                "related_indices": [],
            },
            "pronoun": {
                "pronoun_tag": None,
                "number_tag": None,
                "honorificity": None,
                "case": None,
                "proximity": None,
                "encoding": None,
            },
            "pos": [],
            "composite_flag": False,
            "composite_word": {
                "suffix": None,
                "prefix": None,
                "stand_alone_words": [],
            },
            "special_entity": {
                "definition": None,
                "related_indices": [],
                "space_indices": set(),
                "suffix": None,
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

        # Had to do :(
        sentence = sentence.replace("\n", " ").strip()

        for index in range(len(sentence)):
            if sentence[index] not in punctuations:
                string_buffer += sentence[index]
                end_index = index
                if index == len(sentence) - 1:
                    if string_buffer != "":
                        string_buffer = normalize_token(string_buffer)
                        global_index = (start_index, end_index)
                        if string_buffer not in tokens.keys():
                            tokens[string_buffer] = copy.deepcopy(token)
                        tokens[string_buffer]["punctuation_flag"] = False
                        tokens[string_buffer]["global_index"].append(global_index)
            else:
                if string_buffer != "":
                    string_buffer = normalize_token(string_buffer)
                    global_index = (start_index, end_index)
                    if string_buffer not in tokens.keys():
                        tokens[string_buffer] = copy.deepcopy(token)
                    tokens[string_buffer]["punctuation_flag"] = False
                    tokens[string_buffer]["global_index"].append(global_index)
                    string_buffer = ""

                punctuation_flags.append(index)
                start_index = index + 1
                punctuation = sentence[index]

                if punctuation not in tokens.keys():
                    tokens[punctuation] = copy.deepcopy(token)
                tokens[punctuation]["punctuation_flag"] = True
                idx = (index,index)
                tokens[punctuation]["global_index"].append(idx)
                tokens[punctuation]["pos"] = ["punc"]
        unwanted_token = [" ", None]
        tokens = {k: v for k, v in tokens.items() if k not in unwanted_token}

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
            "বিশেষণ": "adjective",
            "বিশেষ্য": "noun",
            "সর্বনাম": "pronoun",
            "অব্যয়": "conjunction",
            "ক্রিয়া": "verb",
            "ক্রিয়াবিশেষণ": "adverb",
            "ক্রিয়াবিশেষ্য": "adverb",
            "obboy": "conjunction",
            "kriya": "ক্রিয়া",
            "bisheshon": "বিশেষণ",
            "pronoun":"pronoun",
            "verb": "verb"
        }

        analyzed_res = self.analyze_sentence(sentence)
        res = self.utils.getSortedObjectList(analyzed_res)

        # with open("./testing-souhardya.json", "w", encoding="utf-8") as f:
        #     json.dump(res, f, ensure_ascii=False,
        #               default=self.utils.serializeSets, indent=4)
        word_objects = []
        pos_list = []
        already_covered_words = []

        for word_obj in res:
            word = word_obj["word"]
            body = word_obj
            pos = ["undefined"]

            indexes = body["global_index"]
            for global_index in indexes:
                if global_index not in already_covered_words:
                    if "verb" in word_obj:
                        pos = []
                        if "pos" in body:
                            for p in body["pos"]:
                                pos.append(bangla_pos_to_english_pos[p])

                        if "tp" in body["verb"]:
                            pos.append("finite_verb")

                        if (
                            "non_finite" in body["verb"]
                            and body["verb"]["non_finite"] == True
                        ):
                            pos.append("non_finite_verb")

                        related_indexes = word_obj["verb"]["related_indices"]
                        related_indexes.sort(key=lambda x: x[0])
                        for related_index in related_indexes:
                            if (
                                related_index not in word_obj["Orginal_Global_Index"]
                                and related_index not in already_covered_words
                            ):
                                relatedWord = self.utils.getRelatedWords(
                                    analyzed_res, related_index, global_index
                                )
                                if relatedWord != -1:
                                    already_covered_words.append(related_index)
                                    break

                    elif "pronoun" in body:
                        pos = ["pronoun"]
                        if "pos" in body:
                            for p in body["pos"]:
                                pos.append(bangla_pos_to_english_pos[p])

                    elif (
                        "punctuation_flag" in body and body["punctuation_flag"] == True
                    ):
                        pos = ["punctuation"]

                    elif "pos" in body:
                        t = []
                        for p in body["pos"]:
                            t.append(bangla_pos_to_english_pos[p])
                        pos = t

                    already_covered_words.append(global_index)
                    if type(global_index) is list:
                        word_objects.append({"pos": pos, "index": global_index[0]})
                    else:
                        word_objects.append({"pos": pos, "index": global_index})

        word_objects.sort(key=self.utils.sortFunc)

        for entry in word_objects:
            pos_list.append(entry["pos"])

        return pos_list

    def lemmatize_sentence(self, sentence, pure_lemmatize=True):
        # res = self.utils.sortResponse(res)
        word_objects = []
        word_list = []
        already_covered_words = []

        analyzed_res = self.analyze_sentence(sentence)
        res = self.utils.getSortedObjectList(analyzed_res)
        for word_obj in res:
            word = word_obj["word"]
            indexes = word_obj["global_index"]

            special_entity_suffix = ""
            if "special_entity" in word_obj:
                special_entity = word_obj["special_entity"]
                if "suffix" in special_entity:
                    special_entity_suffix = special_entity["suffix"]

            for global_index in indexes:
                words = []
                if global_index not in already_covered_words:
                    if "verb" in word_obj:
                        full_word = word
                        useOriginalWord = False
                        related_indexes = word_obj["verb"]["related_indices"]
                        related_indexes.sort(key=lambda x: x[0])
                        for related_index in related_indexes:
                            if (
                                related_index not in word_obj["Orginal_Global_Index"]
                                and related_index not in already_covered_words
                            ):
                                relatedWord = self.utils.getRelatedWords(
                                    analyzed_res, related_index, global_index
                                )
                                if relatedWord != -1:
                                    already_covered_words.append(related_index)
                                    full_word = full_word + " " + relatedWord
                                    useOriginalWord = True
                                    break

                        if useOriginalWord:
                            words.append(full_word)
                        else:
                            words.append(word_obj["verb"]["parent_verb"][-1])
                            if "emphasizer" in word_obj["verb"]:
                                for emphasizer in word_obj["verb"]["emphasizer"]:
                                    words.append(emphasizer)

                    elif "composite_word" in word_obj:
                        if pure_lemmatize:
                            if "stand_alone_words" in word_obj["composite_word"]:
                                composite_word = ""
                                for word in word_obj["composite_word"][
                                    "stand_alone_words"
                                ]:
                                    composite_word = composite_word + word
                                words.append(composite_word)
                        else:
                            if "prefix" in word_obj["composite_word"]:
                                words.append(word_obj["composite_word"]["prefix"])

                            if "stand_alone_words" in word_obj["composite_word"]:
                                words.append(
                                    word_obj["composite_word"]["stand_alone_words"]
                                )

                            if "suffix" in word_obj["composite_word"]:
                                words.append(word_obj["composite_word"]["suffix"])

                    else:
                        if special_entity_suffix != "":
                            word = word[0 : -len(special_entity_suffix)]
                        words.append(word)

                    already_covered_words.append(global_index)

                    if type(global_index) is list:
                        word_objects.append({"lemma": words, "index": global_index[0]})
                    else:
                        word_objects.append({"lemma": words, "index": global_index})

        word_objects.sort(key=self.utils.sortFunc)

        for word_object in word_objects:
            word_list.append(word_object["lemma"])
        return word_list
