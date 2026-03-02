import json
import os

BIBLE_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
    "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

def load_json(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    base_path = r'd:\Documents\Notes\JavaScript\work_space\bible\versions'
    by_path = os.path.join(base_path, 'by_flat.json')
    en_ust_path = os.path.join(base_path, 'en_ust_flat.json')
    kjv_path = os.path.join(base_path, 'kjv_flat.json')

    print("Loading versions...")
    by_data = load_json(by_path).get('books', {})
    en_ust_data = load_json(en_ust_path).get('books', {})
    kjv_data = load_json(kjv_path).get('books', {})

    # Use specified order, but also catch any extra books if they exist
    found_books = set(by_data.keys()) | set(en_ust_data.keys()) | set(kjv_data.keys())
    ordered_books = [b for b in BIBLE_BOOKS if b in found_books]
    extra_books = sorted(list(found_books - set(BIBLE_BOOKS)))
    final_book_list = ordered_books + extra_books

    merged_bible = {"books": {}}

    print("Merging verses...")
    for book in final_book_list:
        merged_bible["books"][book] = {}
        
        # Collect all chapters for this book across all versions
        chapters_set = set(by_data.get(book, {}).keys()) | \
                       set(en_ust_data.get(book, {}).keys()) | \
                       set(kjv_data.get(book, {}).keys())
        
        # Sort chapters numerically
        sorted_chaps = sorted(list(chapters_set), key=lambda x: int(x))
        
        for chap in sorted_chaps:
            merged_bible["books"][book][chap] = {}
            
            # Collect all verses for this chapter across all versions
            verses_set = set(by_data.get(book, {}).get(chap, {}).keys()) | \
                         set(en_ust_data.get(book, {}).get(chap, {}).keys()) | \
                         set(kjv_data.get(book, {}).get(chap, {}).keys())
            
            # Sort verses numerically
            sorted_verses = sorted(list(verses_set), key=lambda x: int(x))
            
            for verse in sorted_verses:
                v_by = by_data.get(book, {}).get(chap, {}).get(verse, "")
                v_en = en_ust_data.get(book, {}).get(chap, {}).get(verse, "")
                v_kjv = kjv_data.get(book, {}).get(chap, {}).get(verse, "")
                
                merged_bible["books"][book][chap][verse] = {
                    "BY": v_by,
                    "EN_UST": v_en,
                    "KJV": v_kjv
                }

    output_path = r'd:\Documents\Notes\JavaScript\work_space\bible\merged_bible.json'
    print(f"Saving merged Bible to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_bible, f, ensure_ascii=False, indent=2)

    print(f"Done! Merged {len(final_book_list)} books.")

if __name__ == "__main__":
    main()
