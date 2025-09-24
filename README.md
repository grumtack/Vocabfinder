# Vocabfinder
Extract new vocab from usfm Bible text  
  
Vocabfinder works with the tokenized CCB Bible found at https://github.com/Clear-Bible/Open-Bible-TSVs/blob/main/cmn/OCCB-simplified/token/target_OCCB-simplified_20241022.tsv  
Vocabfinder takes a list of Bible books with known vocabulary as argument 1 and finds new vocabulary from books listed as argument 2. 
  
Usage:  
python vocabfinder.py 'LIST_KNOWN_BOOKS' 'LIST_NEW_BOOKS'  

Example:  
python vocabfinder.py 'MAT MRK LUK JHN ACT' 'PHP' 
