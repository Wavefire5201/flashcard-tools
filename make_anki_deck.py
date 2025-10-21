import json
import random

import genanki


def get_random_model_id() -> int:
    return random.randrange(1 << 30, 1 << 31)


furiganaA = [
    "おおきい／おおきな",
    "ちいさい／ちいさな",
    "おおい",
    "すくない",
    "あたらしい",
    "ふるい",
    "いい／よい",
    "よくない",
    "わるい",
    "しずか（な）",
    "うるさい",
    "きれい（な）",
    "きたない",
    "ひろい",
    "せまい",
    "ひくい",
    "たかい",
    "やすい",
    "おもしろい",
    "ゆうめい（な）",
    "にぎやか（な）",
    "つまらない",
    "むずかしい",
    "やさしい",
    "ながい",
    "みじかい",
    "おいしい",
    "まずい",
]

englishA = [
    "big; large",
    "small",
    "many",
    "few",
    "new",
    "old",
    "good",
    "not good; bad",
    "bad",
    "quiet; peaceful",
    "noisy; disturbing",
    "beautiful; clean",
    "dirty",
    "spacious; wide",
    "small (in area); narrow",
    "low",
    "high; expensive",
    "inexpensive; cheap",
    "interesting; funny",
    "famous",
    "lively",
    "boring",
    "difficult",
    "easy; kind",
    "long",
    "short",
    "delicious",
    "bad tasting",
]

# Define a basic model (template for cards)
my_model = genanki.Model(
    1607392319,
    "Japanese Adjectives Model",
    fields=[
        {"name": "Japanese"},
        {"name": "English"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<div style="font-size: 40px;">{{Japanese}}</div>',
            "afmt": '{{FrontSide}}<hr><div style="font-size: 30px;">{{English}}</div>',
        },
    ],
)

# Create the deck
my_deck = genanki.Deck(
    get_random_model_id(),
    "Japanese Adjectives",
)

# Add all cards
for jp, en in zip(furiganaA, englishA):
    note = genanki.Note(
        model=my_model,
        fields=[jp, en],
    )
    my_deck.add_note(note)

# Optionally add deck package
# genanki.Package(my_deck).write_to_file("Japanese_Adjectives.apkg")

# print("✅ Deck successfully created: Japanese_Adjectives.apkg")


def create_chapter_decks(file_name: str):
    with open(file_name, "r") as f:
        file: dict = json.load(f)

    for chapter_name, topics in file.items():
        print(f"Chapter: {chapter_name}")
        for topic in topics:
            for topic_name, vocab_list in topic.items():
                print(f"    Topic: {topic_name}")
                for vocab_item in vocab_list:
                    kanji = vocab_item.get("kanji", "")
                    furigana = vocab_item.get("furigana", "")
                    english = vocab_item.get("english", "")
                    audio_url = vocab_item.get("audio_url", "")
                    print(f"        {kanji} ({furigana}) - {english} - {audio_url}")


def create_topic_decks(): ...


def main():
    create_chapter_decks("./vol1_extracted.json")


if __name__ == "__main__":
    main()
