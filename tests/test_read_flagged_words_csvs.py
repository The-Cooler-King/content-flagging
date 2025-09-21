import csv
import pathlib
import pytest
import sys

# Add the src directory to sys.path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

from main import read_flagged_words_csvs


def create_csv_file(tmp_path, filename, rows):
    """Helper to create a CSV file with given rows."""
    file_path = tmp_path / filename
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return file_path


def test_read_flagged_words_csvs_basic(tmp_path):
    # Arrange
    create_csv_file(tmp_path, "profanity.csv", [["badword"], ["worseword"]])
    create_csv_file(tmp_path, "slang.csv", [["cool"], ["rad"]])

    # Act
    result = read_flagged_words_csvs(str(tmp_path))

    # Assert
    assert isinstance(result, dict)
    assert set(result.keys()) == {"profanity", "slang"}
    assert result["profanity"] == {"badword", "worseword"}
    assert result["slang"] == {"cool", "rad"}


def test_read_flagged_words_csvs_empty_file(tmp_path):
    # Arrange
    create_csv_file(tmp_path, "empty.csv", [])

    # Act
    result = read_flagged_words_csvs(str(tmp_path))

    # Assert
    assert "empty" in result
    assert result["empty"] == set()


def test_read_flagged_words_csvs_ignores_empty_lines(tmp_path):
    # Arrange
    create_csv_file(tmp_path, "mixed.csv", [["word1"], [], ["word2"], ["   "], [""]])  # some empty/whitespace lines

    # Act
    result = read_flagged_words_csvs(str(tmp_path))

    # Assert
    assert result["mixed"] == {"word1", "word2"}


def test_read_flagged_words_csvs_trims_and_lowercases(tmp_path):
    # Arrange
    create_csv_file(tmp_path, "format.csv", [["  Hello "], ["WORLD "]])

    # Act
    result = read_flagged_words_csvs(str(tmp_path))

    # Assert
    assert result["format"] == {"hello", "world"}
