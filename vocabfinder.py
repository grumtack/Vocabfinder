#!/usr/bin/env python3
"""
vocabfind.py - Bible Vocabulary Finder

This script compares vocabulary between different sets of Bible books.
It finds unique vocabulary in the second set that doesn't appear in the first set.

Usage:
    python vocabfind.py "MAT MRK LUK ACT ROM" "GAL PHP"
    python vocabfind.py "GEN EXO LEV" "MAT MRK LUK"
"""

import sys
import csv
from collections import defaultdict

# USFM to book number mapping
USFM_TO_BOOK_NUM = {
    # Old Testament
    'GEN': '01', 'EXO': '02', 'LEV': '03', 'NUM': '04', 'DEU': '05',
    'JOS': '06', 'JDG': '07', 'RUT': '08', '1SA': '09', '2SA': '10',
    '1KI': '11', '2KI': '12', '1CH': '13', '2CH': '14', 'EZR': '15',
    'NEH': '16', 'EST': '17', 'JOB': '18', 'PSA': '19', 'PRO': '20',
    'ECC': '21', 'SNG': '22', 'ISA': '23', 'JER': '24', 'LAM': '25',
    'EZK': '26', 'DAN': '27', 'HOS': '28', 'JOL': '29', 'AMO': '30',
    'OBA': '31', 'JON': '32', 'MIC': '33', 'NAM': '34', 'HAB': '35',
    'ZEP': '36', 'HAG': '37', 'ZEC': '38', 'MAL': '39',
    
    # New Testament
    'MAT': '40', 'MRK': '41', 'LUK': '42', 'JHN': '43', 'ACT': '44',
    'ROM': '45', '1CO': '46', '2CO': '47', 'GAL': '48', 'EPH': '49',
    'PHP': '50', 'COL': '51', '1TH': '52', '2TH': '53', '1TI': '54',
    '2TI': '55', 'TIT': '56', 'PHM': '57', 'HEB': '58', 'JAS': '59',
    '1PE': '60', '2PE': '61', '1JN': '62', '2JN': '63', '3JN': '64',
    'JUD': '65', 'REV': '66'
}

def parse_arguments():
    """Parse command line arguments."""
    if len(sys.argv) != 3:
        print("Usage: python vocabfind.py \"BOOK1 BOOK2 ...\" \"BOOK3 BOOK4 ...\"")
        print("Example: python vocabfind.py \"MAT MRK LUK ACT ROM\" \"GAL PHP\"")
        sys.exit(1)
    
    first_books = sys.argv[1].split()
    second_books = sys.argv[2].split()
    
    return first_books, second_books

def validate_books(books):
    """Validate that all book abbreviations are recognized."""
    invalid_books = [book for book in books if book not in USFM_TO_BOOK_NUM]
    if invalid_books:
        print(f"Error: Unrecognized book abbreviations: {', '.join(invalid_books)}")
        print("Valid abbreviations include: GEN, EXO, MAT, MRK, ROM, etc.")
        sys.exit(1)

def get_book_prefixes(books):
    """Convert USFM book abbreviations to book number prefixes."""
    return [USFM_TO_BOOK_NUM[book] for book in books]

def load_vocabulary(filename, book_prefixes):
    """
    Load vocabulary from TSV file for specified books.
    
    Args:
        filename: Path to the TSV file
        book_prefixes: List of book number prefixes (e.g., ['01', '40', '41'])
    
    Returns:
        set: Unique vocabulary words from the specified books
    """
    vocabulary = set()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Skip the header row
            next(file)
            
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) < 8:
                    continue
                
                # Extract fields
                id_field = parts[0]
                text = parts[2]
                exclude = parts[4] if len(parts) > 4 else ''
                
                # Skip if marked for exclusion
                if exclude.strip().lower() == 'y':
                    continue
                
                # Check if this word belongs to one of our target books
                # The source_verse format is like "01001001" (book + chapter + verse)
                if len(id_field) >= 2:
                    book_num = id_field[:2]
                    if book_num in book_prefixes:
                        # Only add non-empty text that isn't punctuation
                        if text.strip() and not text.strip() in '，。；：？！""''（）【】《》':
                            vocabulary.add(text.strip())
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        print("Make sure 'token_OCCB-simplified.tsv' is in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return vocabulary

def main():
    """Main function."""
    print("Bible Vocabulary Finder")
    print("=" * 50)
    
    # Parse arguments
    first_books, second_books = parse_arguments()
    
    # Validate book abbreviations
    validate_books(first_books + second_books)
    
    # Convert to book prefixes
    first_prefixes = get_book_prefixes(first_books)
    second_prefixes = get_book_prefixes(second_books)
    
    print(f"First set of books: {' '.join(first_books)}")
    print(f"Second set of books: {' '.join(second_books)}")
    print()
    
    # Load vocabulary from both sets
    print("Loading vocabulary from first set...")
    first_vocab = load_vocabulary('token_OCCB-simplified.tsv', first_prefixes)
    
    print("Loading vocabulary from second set...")
    second_vocab = load_vocabulary('token_OCCB-simplified.tsv', second_prefixes)
    
    # Find unique vocabulary in second set
    unique_vocab = second_vocab - first_vocab
    
    # Display results
    print(f"\nVocabulary Statistics:")
    print(f"Words in first set: {len(first_vocab)}")
    print(f"Words in second set: {len(second_vocab)}")
    print(f"Unique words in second set: {len(unique_vocab)}")
    
    if unique_vocab:
        print(f"\nUnique vocabulary found in {' '.join(second_books)}:")
        print("-" * 40)
        
        # Sort the unique vocabulary for better readability
        sorted_vocab = sorted(unique_vocab)
        
        # Print in columns for better formatting
        for i, word in enumerate(sorted_vocab, 1):
            print(f"{word:<10}", end="")
            if i % 6 == 0:  # 6 words per line
                print()
        
        if len(sorted_vocab) % 6 != 0:
            print()  # Final newline if needed
            
        print(f"\nTotal unique words: {len(unique_vocab)}")
    else:
        print(f"\nNo unique vocabulary found in {' '.join(second_books)}.")
        print("All words in the second set also appear in the first set.")

if __name__ == "__main__":
    main()
