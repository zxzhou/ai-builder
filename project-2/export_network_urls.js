/**
 * JavaScript snippet to extract image URLs from browser Network tab
 * 
 * Instructions:
 * 1. Open Instagram profile in Chrome/Firefox
 * 2. Open Developer Tools (F12 or Cmd+Option+I)
 * 3. Go to Network tab
 * 4. Filter by "Img" or search for "cdninstagram"
 * 5. Scroll through the entire profile to load all images
 * 6. Right-click in Network tab → "Save all as HAR with content"
 * 7. Run this script in browser console, or use the Python script to parse HAR file
 * 
 * Or paste this in browser console after scrolling:
 */

(function() {
    const imageUrls = new Set();
    
    // Get all network requests from performance API
    if (window.performance && window.performance.getEntriesByType) {
        const entries = window.performance.getEntriesByType('resource');
        entries.forEach(entry => {
            if (entry.initiatorType === 'img' || 
                (entry.name && (entry.name.includes('instagram.com') || entry.name.includes('cdninstagram.com')))) {
                if (entry.name && !entry.name.includes('avatar') && !entry.name.includes('/s150x150/')) {
                    imageUrls.add(entry.name);
                }
            }
        });
    }
    
    // Also check all img elements
    document.querySelectorAll('img').forEach(img => {
        const src = img.src || img.getAttribute('data-src');
        if (src && (src.includes('instagram.com') || src.includes('cdninstagram.com'))) {
            if (!src.includes('avatar') && !src.includes('/s150x150/')) {
                imageUrls.add(src);
            }
        }
    });
    
    // Output URLs
    console.log('Found', imageUrls.size, 'image URLs:');
    const urlArray = Array.from(imageUrls);
    console.log(JSON.stringify(urlArray, null, 2));
    
    // Copy to clipboard (if possible)
    if (navigator.clipboard) {
        navigator.clipboard.writeText(JSON.stringify(urlArray, null, 2));
        console.log('URLs copied to clipboard!');
    }
    
    return urlArray;
})();

