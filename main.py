from make_anki_deck import create_chapter_decks
from scraper import extract_pages


def main():
    extract_pages("./data/vol1.json", "./data/vol1_extracted.json")
    create_chapter_decks("./data/vol1_extracted.json")


if __name__ == "__main__":
    main()
