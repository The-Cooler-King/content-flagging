import csv
import pathlib
import pdfplumber
import re
from itertools import groupby


def read_flagged_words_csvs(directory: str):
    terms = {}
    dir_path = pathlib.Path(directory)
    # print(f"dir_path: {dir_path}")

    for csv_file in dir_path.glob("*.csv"):
        # print(f"csv file: {csv_file}")
        category = csv_file.stem  # e.g., "profanity"
        terms[category] = {}

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip() != "":  # skip empty lines
                    terms[category][row[0].strip().lower()] = row[1]

    return terms


def extract_text_from_pdfs(directory: str):
    """
    Scans the given directory for .pdf files and extracts text from each page.

    Returns a dictionary with:
        key = pdf file name
        value = list of page texts
    """
    dir_path = pathlib.Path(directory)
    pdf_texts = {}

    for pdf_file in dir_path.glob("*.pdf"):
        # print(f"Processing: {pdf_file}")
        with pdfplumber.open(pdf_file) as pdf:
            pages = []
            for page in pdf.pages:
                page_string = page.extract_text().lower() or ""
                page_word_list = re.findall(r"\b\w+\b", page_string)
                pages.append(page_word_list)  # fallback to empty string if page is blank
            pdf_texts[pdf_file.name] = pages

    return pdf_texts


def search_for_words(pdf_texts, words_to_flag):
    flags = {}
    for pdf_file, content in pdf_texts.items():
        for page_number, page_text in enumerate(content):
            for word in page_text:
                for category, word_list in words_to_flag.items():

                    if word in word_list:

                        if pdf_file not in flags:
                            flags[pdf_file] = {}
                        if category not in flags[pdf_file]:
                            flags[pdf_file][category] = {}
                        if word_list[word] not in flags[pdf_file][category]:
                            flags[pdf_file][category][word_list[word]] = {}
                        if word in flags[pdf_file][category][word_list[word]]:
                            flags[pdf_file][category][word_list[word]][word].append(page_number + 1)
                        else:
                            flags[pdf_file][category][word_list[word]][word] = [page_number + 1]

    return flags


def compress_page_list(page_numbers):
    page_numbers = sorted(page_numbers)  # ensures duplicates are consecutive
    result = []
    for num, group in groupby(page_numbers):
        count = sum(1 for _ in group)  # count items in the group
        if count > 1:
            result.append(f"{num}({count})")
        else:
            result.append(str(num))
    return result


nums = [1, 1, 1, 2, 452, 452, 500]
print(compress_page_list(nums))


def generate_report(results: dict) -> str:
    """
    Generate a plain text report from nested dictionary results.

    Schema: {'category': {'subcategory': {'word_to_flag': [list of page numbers]}}}
    """
    lines = []

    for pdf_file, categories in results.items():
        lines.append(f"PDF: {pdf_file}")

        for category, subcategories in categories.items():
            # Count all instances in this category
            cat_count = sum(len(pages) for sub in subcategories.values() for pages in sub.values())
            lines.append(f"{category}: ({cat_count} instance(s))")

            for subcategory, words in subcategories.items():
                # Count all instances in this subcategory
                sub_count = sum(len(pages) for pages in words.values())
                lines.append(f" - {subcategory}: ({sub_count} instance(s))")

                for word, pages in words.items():
                    if pages:
                        pages = compress_page_list(pages)
                        page_list = ", ".join(str(p) for p in pages)
                        lines.append(f"   - {word}: {page_list}")
                    else:
                        lines.append(f"   - {word}: (no occurrences)")

    return "\n".join(lines)


# print(read_flagged_words_csvs("../lists"))
# print(extract_text_from_pdfs("../pdfs"))

# results = search_for_words(
#     pdf_texts=extract_text_from_pdfs("../pdfs"),
#     words_to_flag=read_flagged_words_csvs("../lists")
# )
#
# report = generate_report(results=results)
#
# print(report)


