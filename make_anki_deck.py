import genanki

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
    2059400110,
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
genanki.Package(my_deck).write_to_file("Japanese_Adjectives.apkg")

print("✅ Deck successfully created: Japanese_Adjectives.apkg")
