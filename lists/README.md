# Flagged Word Lists

Use this directory to keep CSV's of flagged words. Here are some rules/tips:
1. The application will only read CSVs, any other file type in this directory will be ignored.
2. Do not put a header row in your CSV
3. Use only the first two columns in your CSV to list your words. Further columns are currently unsupported.
    - Column A: word to flag
    - Column B: subcategory
4. The content flagger allows for multiple lists to be stored here and the filename of the CSV will be considered the category for the flagged word.
    - e.g., If a CSV file is saved in this directory named `profanity.csv` all the words in this CSV will be considered part of the `profanity` category.