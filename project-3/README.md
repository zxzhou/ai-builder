# Search Query Redirect Tool - Project 3

This is Project 3 of the AI Builder collection - a JavaScript tool that enhances your web search experience by redirecting search queries to alternative search engines when results are unsatisfactory.

## Overview

Have you ever been frustrated with search results from one engine and wished you could quickly try another? This tool solves that problem by automatically extracting your current search query and redirecting it to an alternative search engine with a single click or command.

The tool intelligently parses search URLs from major search engines (Google, Bing, DuckDuckGo, Yahoo, etc.) to extract the query parameter, then constructs a new URL for your preferred alternative search engine. It works seamlessly as a bookmarklet, browser extension, or console script.

## Features

- **Automatic Query Extraction**: Extracts search queries from multiple search engines (Google, Bing, DuckDuckGo, Yahoo, Yandex, Baidu, etc.)
- **Multi-Engine Support**: Redirects to various alternative search engines
- **Easy Integration**: Can be used as a bookmarklet, browser extension script, or console command

## Usage

### Method 1: Browser Console

1. Navigate to any search results page (e.g., Google search results)
2. Open browser console (F12 or Cmd+Option+I)
3. Copy and paste the code from `search_redirect.js`
4. Run: `enhanceSearch()` or `SearchRedirect.enhanceSearch()`

### Method 2: Bookmarklet

Create a bookmark with this minified code as the URL:

```javascript
javascript:(function(){const url=new URL(window.location.href);const hostname=url.hostname.toLowerCase();const params={'google.com':'q','bing.com':'q','duckduckgo.com':'q','yahoo.com':'p'};let queryParam=null;for(const[domain,param]of Object.entries(params)){if(hostname.includes(domain)){queryParam=param;break;}}if(!queryParam)queryParam=url.searchParams.get('q')?'q':url.searchParams.get('p')?'p':null;const query=queryParam?url.searchParams.get(queryParam):null;if(query){window.location.href=`https://duckduckgo.com/?q=${encodeURIComponent(query)}`;}else{alert('Could not extract search query.');}})();
```

### Method 3: Browser Extension

Include `search_redirect.js` as a content script in your browser extension manifest.

## API Reference

### `extractSearchQuery()`

Extracts the search query from the current page URL.

```javascript
const query = extractSearchQuery();
console.log(query); // e.g., "your search terms"
```

### `constructSearchUrl(query, searchEngine)`

Constructs a URL for a specific search engine with the given query.

```javascript
const url = constructSearchUrl("example query", "bing");
// Returns: "https://www.bing.com/search?q=example%20query"
```

**Supported search engines:**
- `google`
- `bing`
- `duckduckgo` (default)
- `yahoo`
- `yandex`
- `baidu`
- `ecosia`
- `startpage`
- `brave`
- `qwant`

### `redirectToAlternativeSearch(alternativeEngine)`

Redirects the current search to an alternative search engine.

```javascript
redirectToAlternativeSearch("bing"); // Redirects to Bing
redirectToAlternativeSearch("duckduckgo"); // Redirects to DuckDuckGo
```

### `getAlternativeSearchUrls(query)`

Returns an object with URLs for all alternative search engines.

```javascript
const alternatives = getAlternativeSearchUrls("example query");
console.log(alternatives.google);
console.log(alternatives.bing);
// etc.
```

### `enhanceSearch()`

Main convenience function that extracts the query and redirects to DuckDuckGo by default.

```javascript
enhanceSearch(); // Extracts query and redirects to DuckDuckGo
```

## Examples

### Redirect to a specific search engine

```javascript
// Extract query and redirect to Bing
const query = extractSearchQuery();
if (query) {
    redirectToAlternativeSearch("bing");
}
```

### Get all alternative URLs

```javascript
const query = extractSearchQuery();
if (query) {
    const alternatives = getAlternativeSearchUrls(query);
    console.log("Google:", alternatives.google);
    console.log("Bing:", alternatives.bing);
    console.log("DuckDuckGo:", alternatives.duckduckgo);
}
```

### Custom redirect logic

```javascript
const query = extractSearchQuery();
if (query) {
    // Redirect to Ecosia for eco-friendly searches
    redirectToAlternativeSearch("ecosia");
}
```

## Supported Search Engines (Input)

The tool can extract queries from:
- Google (all domains)
- Bing
- DuckDuckGo
- Yahoo
- Yandex
- Baidu
- Ecosia
- Startpage
- And more (uses common query parameters as fallback)

## Supported Search Engines (Output)

You can redirect to:
- Google
- Bing
- DuckDuckGo
- Yahoo
- Yandex
- Baidu
- Ecosia
- Startpage
- Brave Search
- Qwant

## Browser Compatibility

Works in all modern browsers that support:
- ES6 JavaScript features
- URL and URLSearchParams APIs

## License

Free to use and modify.

