import json
import requests


def extract_pages(path: str):
    with open(path, "r") as f:
        file = json.load(f)


def extract_vocab(url: str):
    data = requests.get(url)


def main():
    print("Hello from anki-helper!")


if __name__ == "__main__":
    main()
