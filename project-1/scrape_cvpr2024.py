#!/usr/bin/env python3
"""
CVPR 2024 Paper Scraper
Extracts paper titles, authors, abstracts, and PDF/supplementary material links
from the CVPR 2024 Open Access website.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import os
from urllib.parse import urljoin
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Thread locks for CSV writing and duplicate tracking
csv_lock = Lock()
saved_titles_lock = Lock()

BASE_URL = "https://openaccess.thecvf.com"
MAIN_PAGE_URL = "https://openaccess.thecvf.com/CVPR2024?day=all"


def get_page_content(url: str) -> Optional[BeautifulSoup]:
    """Fetch and parse a webpage."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_authors(dd_tag) -> List[str]:
    """Extract author names from a dd tag containing author forms."""
    authors = []
    forms = dd_tag.find_all('form', class_='authsearch')
    for form in forms:
        author_input = form.find('input', {'name': 'query_author'})
        if author_input and author_input.get('value'):
            authors.append(author_input['value'])
    return authors


def extract_links(dd_tag) -> Dict[str, str]:
    """Extract PDF and supplementary material links from a dd tag."""
    links = {'pdf': '', 'supp': ''}
    
    # Find PDF link
    pdf_link = dd_tag.find('a', href=re.compile(r'/papers/.*\.pdf'))
    if pdf_link:
        links['pdf'] = urljoin(BASE_URL, pdf_link['href'])
    
    # Find supplementary link
    supp_link = dd_tag.find('a', href=re.compile(r'/supplemental/.*\.pdf'))
    if supp_link:
        links['supp'] = urljoin(BASE_URL, supp_link['href'])
    
    return links


def extract_abstract(paper_url: str) -> str:
    """Extract abstract from individual paper page."""
    soup = get_page_content(paper_url)
    if not soup:
        return ""
    
    # Try to find abstract - common patterns in CVPR pages
    abstract = ""
    
    # Look for div with id="abstract" or class containing "abstract"
    abstract_div = soup.find('div', id='abstract')
    if not abstract_div:
        abstract_div = soup.find('div', class_=re.compile(r'.*abstract.*', re.I))
    
    if abstract_div:
        # Get text, removing extra whitespace
        abstract = ' '.join(abstract_div.stripped_strings)
    else:
        # Fallback: look for paragraphs after "Abstract" heading
        for tag in soup.find_all(['h2', 'h3', 'h4', 'strong', 'b']):
            if tag and tag.get_text().strip().lower() == 'abstract':
                # Get next sibling paragraphs
                next_tag = tag.find_next_sibling(['p', 'div'])
                if next_tag:
                    abstract = ' '.join(next_tag.stripped_strings)
                    break
    
    return abstract


def extract_paper_basic_info(dt_tag, existing_titles: set) -> Optional[Dict]:
    """Extract basic paper info (title, authors, links) from main page."""
    try:
        # Extract title and paper URL
        title_link = dt_tag.find('a')
        if not title_link:
            return None
        
        title = title_link.get_text().strip()
        
        # Skip if already scraped
        if title in existing_titles:
            return None
        
        paper_relative_url = title_link.get('href', '')
        paper_url = urljoin(BASE_URL, paper_relative_url) if paper_relative_url else ""
        
        # Get the next dd tags (authors and links)
        next_dd_tags = []
        current = dt_tag.find_next_sibling()
        while current and current.name == 'dd':
            next_dd_tags.append(current)
            current = current.find_next_sibling()
        
        # Extract authors (first dd tag usually contains authors)
        authors = []
        pdf_link = ""
        supp_link = ""
        
        for dd_tag in next_dd_tags:
            # Check if this dd contains author forms
            if dd_tag.find('form', class_='authsearch'):
                authors = extract_authors(dd_tag)
            
            # Check if this dd contains links
            if dd_tag.find('a', href=re.compile(r'\.pdf')):
                links = extract_links(dd_tag)
                pdf_link = links['pdf']
                supp_link = links['supp']
        
        return {
            'title': title,
            'authors': ', '.join(authors),
            'author_count': len(authors),
            'abstract': '',  # Will be filled later
            'pdf_link': pdf_link,
            'supp_link': supp_link,
            'paper_url': paper_url
        }
    except Exception as e:
        print(f"Error extracting basic info: {e}")
        return None


def fetch_abstract_with_index(paper_data: Dict, index: int, total: int) -> Tuple[int, Dict]:
    """Fetch abstract for a paper and return with its index."""
    title = paper_data['title']
    paper_url = paper_data['paper_url']
    
    print(f"[{index}/{total}] Fetching abstract: {title[:60]}...")
    abstract = ""
    if paper_url:
        abstract = extract_abstract(paper_url)
    
    paper_data['abstract'] = abstract
    print(f"  ✓ [{index}/{total}] Got abstract ({len(abstract)} chars) for: {title[:60]}...")
    return index, paper_data


def scrape_papers(save_incrementally: bool = True, csv_filename: str = 'cvpr2024_papers.csv', 
                  max_workers: int = 10) -> List[Dict]:
    """Main function to scrape all papers from the CVPR 2024 page using parallel requests."""
    print("Fetching main page...")
    soup = get_page_content(MAIN_PAGE_URL)
    
    if not soup:
        print("Failed to fetch main page!")
        return []
    
    # Check for existing progress
    existing_titles = get_existing_titles(csv_filename)
    if existing_titles:
        print(f"Found {len(existing_titles)} already scraped papers. Will skip duplicates.")
    
    # Track titles we've saved in this run to avoid duplicates
    saved_in_this_run = set()
    
    # Find all paper entries - they're in dt tags with class "ptitle"
    paper_dt_tags = soup.find_all('dt', class_='ptitle')
    
    print(f"Found {len(paper_dt_tags)} papers.")
    print("Step 1: Extracting basic info (title, authors, links) from main page...")
    
    # Step 1: Extract all basic info quickly from main page
    papers_basic = []
    skipped_count = 0
    
    for idx, dt_tag in enumerate(paper_dt_tags, 1):
        paper_data = extract_paper_basic_info(dt_tag, existing_titles)
        if paper_data:
            papers_basic.append((idx, paper_data))
        else:
            skipped_count += 1
    
    papers_to_fetch = [p for _, p in papers_basic]
    print(f"Extracted basic info for {len(papers_to_fetch)} papers ({skipped_count} skipped).")
    
    if not papers_to_fetch:
        print("No new papers to fetch!")
        return []
    
    # Step 2: Fetch abstracts in parallel
    print(f"\nStep 2: Fetching abstracts in parallel (using {max_workers} workers)...")
    papers_with_abstracts = {}
    
    # Use ThreadPoolExecutor for parallel abstract fetching
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_index = {
            executor.submit(fetch_abstract_with_index, paper_data, idx, len(papers_basic)): idx
            for idx, paper_data in papers_basic
        }
        
        # Process completed tasks
        completed = 0
        for future in as_completed(future_to_index):
            try:
                index, paper_data = future.result()
                papers_with_abstracts[index] = paper_data
                completed += 1
                
                # Save incrementally (only if not already saved)
                if save_incrementally:
                    title = paper_data['title']
                    with saved_titles_lock:
                        if title not in saved_in_this_run:
                            append_mode = os.path.exists(csv_filename) or len(existing_titles) > 0
                            save_to_csv([paper_data], csv_filename, append=append_mode, verbose=False)
                            saved_in_this_run.add(title)
                
                if completed % 50 == 0:
                    print(f"  Progress: {completed}/{len(papers_basic)} abstracts fetched...")
            except Exception as e:
                idx = future_to_index[future]
                print(f"  ✗ Error fetching abstract for paper {idx}: {e}")
    
    # Sort by index and return
    papers = [papers_with_abstracts[idx] for idx in sorted(papers_with_abstracts.keys())]
    
    print(f"\nSuccessfully extracted {len(papers)} papers!")
    return papers


def save_to_csv(papers: List[Dict], filename: str = 'cvpr2024_papers.csv', append: bool = False, verbose: bool = False):
    """Save extracted papers to CSV file (thread-safe)."""
    if not papers:
        if verbose:
            print("No papers to save!")
        return
    
    fieldnames = ['title', 'authors', 'author_count', 'abstract', 'pdf_link', 'supp_link', 'paper_url']
    
    # Thread-safe CSV writing
    with csv_lock:
        mode = 'a' if append else 'w'
        file_exists = os.path.exists(filename)
        
        with open(filename, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Only write header if file is new or we're not appending
            if not append or not file_exists:
                writer.writeheader()
            writer.writerows(papers)
    
    if verbose:
        print(f"Saved {len(papers)} papers to {filename}")


def get_existing_titles(filename: str = 'cvpr2024_papers.csv') -> set:
    """Get set of already scraped paper titles to avoid duplicates."""
    existing_titles = set()
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_titles.add(row['title'])
    except FileNotFoundError:
        pass
    return existing_titles


def main():
    """Main execution function."""
    print("=" * 60)
    print("CVPR 2024 Paper Scraper (Parallel Version)")
    print("=" * 60)
    
    csv_filename = 'cvpr2024_papers_2.csv'
    # Use 10-15 workers for parallel requests (adjust based on your connection)
    max_workers = 15
    print(f"Using {max_workers} parallel workers for faster extraction.\n")
    
    papers = scrape_papers(save_incrementally=True, csv_filename=csv_filename, max_workers=max_workers)
    
    # Note: When save_incrementally=True, papers are already saved during extraction
    # So we don't need to save again here to avoid duplicates
    
    # Count total papers in CSV
    try:
        with open(csv_filename, 'r', encoding='utf-8') as f:
            total_count = sum(1 for _ in csv.DictReader(f))
        print(f"\n✓ Scraping complete! Total papers in CSV: {total_count}")
        if papers:
            print(f"  (Extracted {len(papers)} new papers, already saved incrementally)")
    except FileNotFoundError:
        if papers:
            # If file doesn't exist and we have papers, save them now
            save_to_csv(papers, csv_filename, append=False, verbose=True)
            print(f"\n✓ Scraping complete! Saved {len(papers)} papers to {csv_filename}")
        else:
            print("\n✗ No papers were extracted. Please check the website URL and your internet connection.")


if __name__ == "__main__":
    main()

