# CVPR 2024 Paper Scraper - Project 1

This is Project 1 of the AI Builder collection - a web scraper to extract paper information from the CVPR 2024 Open Access website.

## Overview

This Python script scrapes data from `https://openaccess.thecvf.com/CVPR2024?day=all` and saves the extracted information into a CSV file for easy analysis and reference.

## Features

- **Parallel Processing**: Uses 15 concurrent workers for fast abstract extraction
- **Incremental Saving**: Progress is saved as the script runs, so you can resume if interrupted
- **Duplicate Prevention**: Automatically skips already scraped papers
- **Complete Data**: Extracts titles, authors, abstracts, PDF links, and supplementary material links

## Project Structure

```
project-1/
├── scrape_cvpr2024.py    # Main scraper script
├── remove_duplicates.py   # Utility to remove duplicates from CSV
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Scraper

```bash
python scrape_cvpr2024.py
```

The script will:
1. Fetch the main CVPR 2024 page
2. Extract all paper information (titles, authors, links)
3. Visit each paper's detail page in parallel to get abstracts
4. Save results incrementally to `cvpr2024_papers.csv`

**Note**: Since the script visits each paper's page individually, it may take 10-20 minutes depending on the number of papers and network speed (much faster with parallel processing).

### Removing Duplicates

If you need to clean up a CSV file with duplicates:

```bash
python remove_duplicates.py input_file.csv output_file.csv
```

## Output Format

The CSV file contains one row per paper with the following columns:

| Column | Description |
|--------|-------------|
| title | Paper title |
| authors | Comma-separated list of authors |
| author_count | Number of authors |
| abstract | Paper abstract |
| pdf_link | Direct link to PDF |
| supp_link | Link to supplementary materials (if available) |
| paper_url | Link to the paper's detail page |

## Technical Details

### How It Works

1. **Main Page Parsing**: Fetches and parses the main CVPR 2024 page to extract basic paper information
2. **Parallel Abstract Extraction**: Uses ThreadPoolExecutor with 15 workers to fetch abstracts concurrently
3. **Incremental Saving**: Each paper is saved immediately after extraction to preserve progress
4. **Duplicate Prevention**: Tracks already scraped papers to avoid duplicates

### Libraries Used

- **requests**: HTTP library for fetching web pages
- **beautifulsoup4**: HTML parsing library
- **lxml**: Fast XML/HTML parser (used by BeautifulSoup)
- **concurrent.futures**: For parallel processing

### Performance

- **Sequential (old)**: ~22+ minutes minimum, often hours
- **Parallel (current)**: ~10-20 minutes for 2,000+ papers

## Troubleshooting

- **No papers extracted**: Check your internet connection and verify the website URL is accessible
- **Missing abstracts**: The website structure may have changed; check the HTML structure of a paper page
- **Timeout errors**: Increase the timeout value in `get_page_content()` or check your network connection
- **Duplicates**: Use `remove_duplicates.py` to clean up the CSV file

## License

This project is part of the AI Builder collection.
