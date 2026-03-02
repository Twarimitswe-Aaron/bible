import json
import os

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_verses(data):
    verses = {}
    for book_name, book_data in data.get('books', {}).items():
        for chap_num, chap_data in book_data.items():
            for verse_num, verse_text in chap_data.items():
                verses[(book_name, int(chap_num), int(verse_num))] = verse_text
    return verses

def main():
    base_path = r'd:\Documents\Notes\JavaScript\work_space\bible\versions'
    by_path = os.path.join(base_path, 'by_flat.json')
    en_ust_path = os.path.join(base_path, 'en_ust_flat.json')
    kjv_path = os.path.join(base_path, 'kjv_flat.json')

    by_data = load_json(by_path)
    en_ust_data = load_json(en_ust_path)
    kjv_data = load_json(kjv_path)

    by_verses = get_verses(by_data)
    en_ust_verses = get_verses(en_ust_data)
    kjv_verses = get_verses(kjv_data)

    all_keys = sorted(set(by_verses.keys()) | set(en_ust_verses.keys()) | set(kjv_verses.keys()), 
                      key=lambda x: (x[0], x[1], x[2]))

    mismatches = []
    for key in all_keys:
        in_by = key in by_verses
        in_en = key in en_ust_verses
        in_kjv = key in kjv_verses
        
        if not (in_by and in_en and in_kjv):
            mismatches.append({
                'Book': key[0],
                'Chap': key[1],
                'Verse': key[2],
                'BY': 'OK' if in_by else 'Missing',
                'EN_UST': 'OK' if in_en else 'Missing',
                'KJV': 'OK' if in_kjv else 'Missing'
            })

    output_path = r'd:\Documents\Notes\JavaScript\work_space\bible\mismatch_report.txt'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        header = f"{'Book':<20} | {'Chap':<5} | {'Verse':<5} | {'BY':<10} | {'EN_UST':<10} | {'KJV':<10}"
        f.write(header + '\n')
        f.write("-" * len(header) + '\n')
        
        for m in mismatches:
            line = f"{m['Book']:<20} | {m['Chap']:<5} | {m['Verse']:<5} | {m['BY']:<10} | {m['EN_UST']:<10} | {m['KJV']:<10}"
            f.write(line + '\n')
            
        f.write("-" * len(header) + '\n')
        f.write(f"Total Mismatched Verses: {len(mismatches)}\n")

    print(f"Report generated: {output_path}")
    print(f"Total Mismatched Verses: {len(mismatches)}")

if __name__ == "__main__":
    main()
