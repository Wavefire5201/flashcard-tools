import json
import re

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://laits.utexas.edu/japanese/joshu/vocabulary/vocabflashcard/"


def extract_vocab_page(metadata: dict) -> dict:
    """Scrape kanjiA, furiganaA, englishA, and audioA arrays from a vocab HTML page."""

    response = requests.get(BASE_URL + metadata["url"])
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Only select chunk that contains the data
    js_text = ""
    for script in soup.find_all("script"):
        if "kanjiA" in script.text:
            js_text = script.text
            break

    if not js_text:
        raise ValueError("No script tag containing the vocab was found.")

    def extract_array(name):
        pattern = rf"{name}\s*=\s*new Array\s*\((.*?)\);"
        match = re.search(pattern, js_text, re.DOTALL)
        if not match:
            return []

        raw = match.group(1)
        # Clean full-width commas/spaces + normalize text
        raw = raw.replace("，", ",").replace("　", " ")
        # Capture both single & double quoted strings
        items = re.findall(r"'(.*?)'|\"(.*?)\"", raw)
        values = [a or b for a, b in items]
        return [v.strip() for v in values if v.strip()]

    kanji = extract_array("kanjiA")
    furigana = extract_array("furiganaA")
    english = extract_array("englishA")
    audio_url = extract_array("audioA")

    result = [
        {
            "kanji": kanji[i] if i < len(kanji) else "",
            "furigana": furigana[i] if i < len(furigana) else "",
            "english": english[i] if i < len(english) else "",
            "audio_url": audio_url[i][3:] if i < len(audio_url) else "",
        }
        for i in range(max(len(kanji), len(furigana), len(english), len(audio_url)))
    ]

    return {metadata["title"]: result}


def extract_pages(path: str, save_path: str):
    chapters = {}
    with open(path, "r", encoding="utf-8") as f:
        data: dict[str, list] = json.load(f)
        for chapter, lst in data.items():
            chapter_vocab = []
            for topic in lst:
                extracted = extract_vocab_page(topic)
                chapter_vocab.append(extracted)
            chapters[chapter] = chapter_vocab

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(chapters, f, indent=2)


def main():
    extract_pages("./data/vol1.json", "./data/vol1_extracted.json")


if __name__ == "__main__":
    main()
