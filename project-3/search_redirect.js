/**
 * Search Query Redirect Tool
 * 
 * This tool enhances web search experience by redirecting search queries
 * to alternative search engines when results are unsatisfactory.
 * 
 * Usage:
 * - As a bookmarklet: Copy the minified version and save as a bookmark
 * - As a browser extension: Include in your extension's content script
 * - In browser console: Run the function directly
 */

/**
 * Extracts the search query from the current page URL
 * Supports multiple search engines: Google, Bing, DuckDuckGo, Yahoo, etc.
 * 
 * @returns {string|null} The extracted search query, or null if not found
 */
function extractSearchQuery() {
    const url = new URL(window.location.href);
    const hostname = url.hostname.toLowerCase();
    
    // Map of search engines and their query parameter names
    const searchEngineParams = {
        'google.com': 'q',
        'google.co.uk': 'q',
        'google.ca': 'q',
        'bing.com': 'q',
        'duckduckgo.com': 'q',
        'yahoo.com': 'p',
        'yandex.com': 'text',
        'baidu.com': 'wd',
        'ecosia.org': 'q',
        'startpage.com': 'q',
        'ask.com': 'q',
        'aol.com': 'q',
        'search.yahoo.com': 'p'
    };
    
    // Find the appropriate parameter name for the current search engine
    let queryParam = null;
    
    for (const [domain, param] of Object.entries(searchEngineParams)) {
        if (hostname.includes(domain)) {
            queryParam = param;
            break;
        }
    }
    
    // If no specific match, try common parameters
    if (!queryParam) {
        queryParam = url.searchParams.get('q') ? 'q' : 
                    url.searchParams.get('p') ? 'p' : 
                    url.searchParams.get('query') ? 'query' : null;
    }
    
    if (queryParam) {
        const query = url.searchParams.get(queryParam);
        return query ? decodeURIComponent(query) : null;
    }
    
    return null;
}

/**
 * Constructs a URL for an alternative search engine with the given query
 * 
 * @param {string} query - The search query to use
 * @param {string} searchEngine - The target search engine (default: 'duckduckgo')
 * @returns {string} The constructed search URL
 */
function constructSearchUrl(query, searchEngine = 'duckduckgo') {
    const encodedQuery = encodeURIComponent(query);
    
    const searchEngineUrls = {
        'google': `https://www.google.com/search?q=${encodedQuery}`,
        'bing': `https://www.bing.com/search?q=${encodedQuery}`,
        'duckduckgo': `https://duckduckgo.com/?q=${encodedQuery}`,
        'yahoo': `https://search.yahoo.com/search?p=${encodedQuery}`,
        'yandex': `https://yandex.com/search/?text=${encodedQuery}`,
        'baidu': `https://www.baidu.com/s?wd=${encodedQuery}`,
        'ecosia': `https://www.ecosia.org/search?q=${encodedQuery}`,
        'startpage': `https://www.startpage.com/sp/search?query=${encodedQuery}`,
        'brave': `https://search.brave.com/search?q=${encodedQuery}`,
        'qwant': `https://www.qwant.com/?q=${encodedQuery}`
    };
    
    const normalizedEngine = searchEngine.toLowerCase();
    
    if (searchEngineUrls[normalizedEngine]) {
        return searchEngineUrls[normalizedEngine];
    }
    
    // Default to DuckDuckGo if engine not found
    console.warn(`Search engine "${searchEngine}" not found. Defaulting to DuckDuckGo.`);
    return searchEngineUrls['duckduckgo'];
}

/**
 * Redirects the current search to an alternative search engine
 * 
 * @param {string} alternativeEngine - The target search engine (default: 'duckduckgo')
 * @returns {boolean} True if redirect was successful, false otherwise
 */
function redirectToAlternativeSearch(alternativeEngine = 'duckduckgo') {
    const query = extractSearchQuery();
    
    if (!query) {
        console.error('Could not extract search query from current URL.');
        alert('Could not extract search query from current URL. Please make sure you are on a search results page.');
        return false;
    }
    
    const newUrl = constructSearchUrl(query, alternativeEngine);
    console.log(`Redirecting search "${query}" to ${alternativeEngine}: ${newUrl}`);
    window.location.href = newUrl;
    
    return true;
}

/**
 * Convenience function to cycle through alternative search engines
 * Provides a list of alternative engines for the current query
 * 
 * @param {string} query - The search query
 * @returns {Object} Object containing URLs for various search engines
 */
function getAlternativeSearchUrls(query) {
    const engines = ['google', 'bing', 'duckduckgo', 'yahoo', 'ecosia', 'startpage', 'brave', 'qwant'];
    const alternatives = {};
    
    engines.forEach(engine => {
        alternatives[engine] = constructSearchUrl(query, engine);
    });
    
    return alternatives;
}

/**
 * Main function that can be called directly
 * Redirects to DuckDuckGo by default, but can be configured
 */
function enhanceSearch() {
    const query = extractSearchQuery();
    
    if (!query) {
        console.error('Could not extract search query from current URL.');
        alert('Could not extract search query from current URL. Please make sure you are on a search results page.');
        return;
    }
    
    // You can change the default alternative engine here
    const defaultAlternative = 'duckduckgo';
    
    // Show available alternatives (optional - can be removed for silent redirect)
    const alternatives = getAlternativeSearchUrls(query);
    console.log('Available alternative search engines:', alternatives);
    
    // Redirect to the default alternative
    redirectToAlternativeSearch(defaultAlternative);
}

// Export functions for use in modules (if using ES6 modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        extractSearchQuery,
        constructSearchUrl,
        redirectToAlternativeSearch,
        getAlternativeSearchUrls,
        enhanceSearch
    };
}

// Make functions available globally for browser console usage
if (typeof window !== 'undefined') {
    window.SearchRedirect = {
        extractSearchQuery,
        constructSearchUrl,
        redirectToAlternativeSearch,
        getAlternativeSearchUrls,
        enhanceSearch
    };
}

