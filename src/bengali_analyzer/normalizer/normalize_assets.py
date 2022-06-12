import os
import json
import glob
import hashlib
from tqdm import tqdm
from termcolor import colored
from bnunicodenormalizer import Normalizer

CHUNK_SIZE = 8192
ENCODING_FORMAT = "utf-8"
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKSUM_DIR = os.path.join(THIS_DIR, "checksum.json")
ERROR_DIR = os.path.join(THIS_DIR, "defective_assets" + os.sep)

error_count = 0


def get_file_name(asset_path):
    return asset_path.split(os.sep)[-1]


def get_file_extension(asset_path):
    return os.path.splitext(asset_path)[1]


def generate_error_report(asset_path, line):
    global error_count

    error_count += 1
    error_dir = os.path.join(ERROR_DIR, get_file_name(asset_path))

    if not os.path.exists(error_dir):
        os.makedirs(error_dir)

    with open(error_dir, "a", encoding=ENCODING_FORMAT) as outfile:
        outfile.write(line)


def file_replace(tmp_path, asset_path):
    if os.path.exists(tmp_path):
        os.replace(tmp_path, asset_path)


def generate_checksum(files):
    checksums = {}

    for asset_path in files:
        with open(asset_path, "rb") as f:
            file_hash = hashlib.blake2b()
            while chunk := f.read(CHUNK_SIZE):
                file_hash.update(chunk)

        checksums[get_file_name(asset_path)] = file_hash.hexdigest()

    return checksums


def normalize_word(word):
    bn_normalizer = Normalizer(allow_english=True)
    normalized_token = bn_normalizer(word)

    return normalized_token["normalized"]


def normalize_sentence(sentence):
    words = sentence.strip().split(" ")

    sentence = ""

    for word in words:
        sentence += str(normalize_word(word=word)) + " "

    return sentence.strip()


# Only csv and txt handled here
def normalize_other(asset_path):
    tmp_path = os.path.join(THIS_DIR, "tmp.txt")

    with open(asset_path, "r", encoding=ENCODING_FORMAT) as f:
        lines = sorted(set(f.readlines()))

        for i, line in enumerate(lines):
            try:
                line = normalize_sentence(sentence=line)

                # after normalizing every line it is being written to tmp file
                with open(tmp_path, "a", encoding=ENCODING_FORMAT) as f2:
                    f2.writelines(line + "\n")
            except:
                # print(
                #     colored(
                #         f"ERROR: In line {i} of file {asset_path}, output: {line}",
                #         "red",
                #     )
                # )

                generate_error_report(asset_path=asset_path, line=line)

    # Replacing the original file after a successful normalization
    file_replace(tmp_path=tmp_path, asset_path=asset_path)


def normalize_json(asset_path):
    tmp_path = os.path.join(THIS_DIR, "tmp.json")

    with open(asset_path, "r", encoding=ENCODING_FORMAT) as f:
        data = json.dumps(json.load(f), ensure_ascii=False)

        data = normalize_sentence(sentence=data)

        # Writing to temporary json
        with open(tmp_path, "w", encoding=ENCODING_FORMAT) as outfile:
            outfile.write(data)

    # Replacing the original file after a successful normalization
    file_replace(tmp_path=tmp_path, asset_path=asset_path)


def get_non_normalized_files(files):
    checksums = generate_checksum(files)

    with open(CHECKSUM_DIR, encoding=ENCODING_FORMAT) as json_file:
        original_checksums = json.load(json_file)

    return [
        c
        for c in checksums
        if c not in original_checksums or original_checksums[c] != checksums[c]
    ]


def normalize(file_dir, ignore_files=[]):
    all_files = glob.glob(file_dir + "*")
    supported_extensions = [".csv", ".CSV", ".txt", ".TXT", ".json", ".JSON"]
    files = [
        files
        for files in all_files
        if get_file_name(files) not in ignore_files
        and get_file_extension(files) in supported_extensions
    ]

    non_normalized_files = get_non_normalized_files(files=files)

    if len(non_normalized_files):
        print(
            colored(
                "One or multiple assets has been changed\nOnly '*.csv', '*.txt' and '*.json' files will be normalized\n\nNormalizing those assets, please wait...",
                "yellow",
            )
        )

        for asset_path in tqdm(non_normalized_files):
            asset_path = os.path.join(file_dir, asset_path)

            if get_file_extension(asset_path) in [".json", ".JSON"]:
                normalize_json(asset_path)
            else:
                normalize_other(asset_path)

        # Update file's checksum
        new_checksum = generate_checksum(files=files)
        with open(CHECKSUM_DIR, "w", encoding=ENCODING_FORMAT) as outfile:
            json.dump(new_checksum, outfile)

        if error_count:
            print(
                colored(
                    f"{error_count} errors occured\nCheck {ERROR_DIR} to identify which type of patterns we can't currently normalize!!!\n",
                    "red",
                )
            )

        print(colored("Normalization completed 🥳🥳🥳\n", "green"))
