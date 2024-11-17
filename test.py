import json
import requests

# Define available versions and their identifiers for the Bible-API
versions = {
    "KJV": "en_kjv.json",  # Local KJV JSON file
    "RVR": "es_rvr.json",  # Local RVR (Spanish) JSON file
    "ASV": "asv",  # API identifier for ASV
    "WEB": "web",  # API identifier for WEB
}

# Mapping of full book names to their abbreviations (adjust this to match your JSON format)
book_abbreviation_map = {
    "Genesis": "gn",
    "Exodus": "ex",
    "Leviticus": "lv",
    "Numbers": "nu",
    "Deuteronomy": "dt",
    "Joshua": "jos",
    "Judges": "jdg",
    "Ruth": "ru",
    "1 Samuel": "1sa",
    "2 Samuel": "2sa",
    "1 Kings": "1ki",
    "2 Kings": "2ki",
    "1 Chronicles": "1ch",
    "2 Chronicles": "2ch",
    "Ezra": "ezr",
    "Nehemiah": "neh",
    "Esther": "est",
    "Job": "job",
    "Psalms": "psa",
    "Proverbs": "pro",
    "Ecclesiastes": "ecc",
    "Song of Solomon": "sos",
    "Isaiah": "isa",
    "Jeremiah": "jer",
    "Lamentations": "lam",
    "Ezekiel": "ezk",
    "Daniel": "dan",
    "Hosea": "hos",
    "Joel": "joe",
    "Amos": "amo",
    "Obadiah": "oba",
    "Jonah": "jon",
    "Micah": "mic",
    "Nahum": "nah",
    "Habakkuk": "hab",
    "Zephaniah": "zep",
    "Haggai": "hag",
    "Zechariah": "zec",
    "Malachi": "mal",
    "Matthew": "mat",
    "Mark": "mrk",
    "Luke": "luk",
    "John": "jhn",
    "Acts": "act",
    "Romans": "rom",
    "1 Corinthians": "1co",
    "2 Corinthians": "2co",
    "Galatians": "gal",
    "Ephesians": "eph",
    "Philippians": "php",
    "Colossians": "col",
    "1 Thessalonians": "1th",
    "2 Thessalonians": "2th",
    "1 Timothy": "1ti",
    "2 Timothy": "2ti",
    "Titus": "tit",
    "Philemon": "phm",
    "Hebrews": "heb",
    "James": "jam",
    "1 Peter": "1pe",
    "2 Peter": "2pe",
    "1 John": "1jn",
    "2 John": "2jn",
    "3 John": "3jn",
    "Jude": "jud",
    "Revelation": "rev"
}

# Load the KJV and RVR JSON files into memory
def load_bible_json(version):
    if version == "KJV":
        with open("en_kjv.json", "r", encoding="utf-8-sig") as file:
            return json.load(file)
    elif version == "RVR":
        with open("es_rvr.json", "r", encoding="utf-8-sig") as file:
            return json.load(file)
    else:
        return None

# Function to retrieve verses from the JSON file (KJV or RVR)
def get_verse_from_json(reference, version):
    # Load the JSON data for the chosen version (KJV or RVR)
    bible_data = load_bible_json(version)
    
    # Parse the reference into book, chapter, and verse
    book, ref = reference.split(' ', 1)
    chapter, verse = ref.split(':')

    # Check if the book exists in the abbreviation map
    if book not in book_abbreviation_map:
        return "Book not found."

    # Get the abbreviation for the book
    book_abbreviation = book_abbreviation_map[book]

    # Find the correct book data
    for book_data in bible_data:
        if book_data["abbrev"] == book_abbreviation:
            try:
                chapter_idx = int(chapter) - 1  # Convert to 0-indexed
                return book_data["chapters"][chapter_idx][int(verse) - 1]
            except IndexError:
                return "Verse not found."
    return "Chapter not found."

# Function to get Bible verses from the Bible-API
def get_bible_verse(reference, translation="web"):
    url = f"https://bible-api.com/{reference}?translation={translation}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "Verse text not found.")
        else:
            return f"Error: Unable to fetch verse. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Main program
def main():
    # Prompt the user to choose a translation
    print(f"Choose from the following Bible versions: {', '.join(versions.keys())}")
    version = input(f"Choose a version: ").strip().upper()

    # Check if the chosen version is valid
    if version not in versions:
        print(f"Invalid version. Please choose from {', '.join(versions.keys())}.")
        return

    # Prompt the user to input a reference (book, chapter, verse, e.g., Romans 12:2)
    reference = input("Enter the Bible reference (e.g., Romans 12:2): ").strip()

    # If the selected version is KJV or RVR, get the verse from the local JSON files
    if version in ["KJV", "RVR"]:
        verse_text = get_verse_from_json(reference, version)
        print(f"{version} ({reference}): {verse_text}")

    # For ASV or WEB, fetch from the Bible-API
    else:
        verse_text = get_bible_verse(reference, versions[version])
        print(f"{version} ({reference}): {verse_text}")

# Run the program
if __name__ == "__main__":
    main()
