#!/usr/bin/env python3
"""
Remove duplicate papers from CSV file based on paper titles.
"""

import csv
import sys
from collections import OrderedDict

def remove_duplicates(input_file: str, output_file: str = None):
    """Remove duplicate papers from CSV file, keeping the first occurrence."""
    if output_file is None:
        output_file = input_file.replace('.csv', '_deduplicated.csv')
    
    seen_titles = set()
    unique_papers = []
    duplicate_count = 0
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            title = row['title']
            if title not in seen_titles:
                seen_titles.add(title)
                unique_papers.append(row)
            else:
                duplicate_count += 1
    
    print(f"Found {duplicate_count} duplicates out of {len(unique_papers) + duplicate_count} total rows.")
    print(f"Writing {len(unique_papers)} unique papers to {output_file}...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_papers)
    
    print(f"✓ Done! Deduplicated file saved as: {output_file}")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_duplicates.py <input_csv_file> [output_csv_file]")
        print("Example: python remove_duplicates.py cvpr2024_papers_2.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    remove_duplicates(input_file, output_file)

