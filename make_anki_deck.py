import json
import os
import random
import urllib.request
from pathlib import Path

import genanki

AUDIO_BASE_URL = "https://laits.utexas.edu/japanese/joshu/vocabulary/vocabflashcard/"

yookosu_vocab_model = genanki.Model(
    1607392320,
    "Vocab Model",
    fields=[
        {"name": "Kanji"},
        {"name": "Furigana"},
        {"name": "English"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Vocab Card",
            "qfmt": '<div style="font-size: 40px;">{{Furigana}} -{{Kanji}}{{Audio}}</div>',
            "afmt": '{{FrontSide}}<hr><div style="font-size: 30px;">{{English}}</div>',
        },
    ],
)


def get_random_model_id() -> int:
    """Generate a random model ID."""
    return random.randrange(1 << 30, 1 << 31)


def download_audio(url: str, output_dir: str) -> str:
    """Download audio file and return the filename."""
    if not url:
        return ""

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Extract filename from URL
    filename = url.split("/")[-1] + ".mp3"
    filepath = os.path.join(output_dir, filename)

    # Download if not already exists
    if not os.path.exists(filepath):
        try:
            urllib.request.urlretrieve(f"{AUDIO_BASE_URL}{url}.mp3", filepath)
            print(f"    Downloaded: {filename}")
        except Exception as e:
            print(f"    Error downloading {url}: {e}")
            return ""

    return filepath


def create_chapter_decks(file_name: str):
    """Create Anki decks for each chapter in the given JSON file."""
    with open(file_name, "r") as f:
        file: dict = json.load(f)

    audio_dir = "./audio_temp"

    for chapter_name, topics in file.items():
        # Generate decks per chapter
        chapter_deck = genanki.Deck(
            get_random_model_id(),
            f"Yookoso Vol.1 - {chapter_name}",
        )
        print(f"Chapter: {chapter_name}")
        media_files = []
        for topic in topics:
            for topic_name, vocab_list in topic.items():
                print(f"    Topic: {topic_name}")
                for vocab_item in vocab_list:
                    kanji = vocab_item.get("kanji", "")
                    furigana = vocab_item.get("furigana", "")
                    english = vocab_item.get("english", "")
                    audio_url = vocab_item.get("audio_url", "")

                    # Download audio file
                    audio_filepath = download_audio(audio_url, audio_dir)

                    # Get just the filename for the note field
                    audio_filename = (
                        os.path.basename(audio_filepath) if audio_filepath else ""
                    )

                    # Format audio reference for Anki
                    audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

                    # Add to media files list
                    if audio_filepath:
                        media_files.append(audio_filepath)

                    # Create note
                    note = genanki.Note(
                        model=yookosu_vocab_model,
                        fields=[kanji, furigana, english, audio_field],
                    )
                    chapter_deck.add_note(note)

                    print(f"        {kanji} ({furigana}) - {english}")

        package = genanki.Package(chapter_deck)
        package.media_files = media_files

        # Ensure output directory exists
        Path("./decks/chapter-decks").mkdir(parents=True, exist_ok=True)

        # Write to file
        output_path = f"./decks/chapter-decks/{chapter_name}.apkg"
        package.write_to_file(output_path)

        print(f"Created chapter deck: {output_path}\n")


def create_topic_decks(file_name: str):
    """Create Anki decks for each topic in the given JSON file."""
