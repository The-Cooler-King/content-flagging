import csv
import pathlib


def read_flagged_words_csvs(directory: str):
    terms = {}
    dir_path = pathlib.Path(directory)
    print(f"dir_path: {dir_path}")

    for csv_file in dir_path.glob("*.csv"):
        print(f"csv file: {csv_file}")
        category = csv_file.stem  # e.g., "profanity"
        terms[category] = set()

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip() != "":  # skip empty lines
                    terms[category].add(row[0].strip().lower())

    return terms


directory_name = "../lists"
print(read_flagged_words_csvs(directory=directory_name))