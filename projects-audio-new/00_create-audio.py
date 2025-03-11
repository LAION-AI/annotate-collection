import asyncio
import aiohttp
import re
import json
from urllib.parse import urljoin

# Base URL of the directory to start from.
BASE_URL = "your-server-url-here"
BASE_URL = f"{BASE_URL}/mnt/weka/home/laion/talent-emotion-bins/"

async def fetch(url, session):
    """Fetches the content of a URL as text."""
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Error fetching {url}: HTTP {response.status}")
            return ""

async def parse_links(html, base_url):
    """
    Parses the HTML to extract href links.
    Filters out parent directory links.
    """
    # Regex to extract href links from anchor tags.
    pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href=["\'](.*?)["\']', re.IGNORECASE)
    raw_links = pattern.findall(html)
    # Build absolute URLs and filter out irrelevant links.
    links = [urljoin(base_url, link) for link in raw_links if link not in ['../', './']]
    return links

async def crawl(url, session, results):
    """
    Recursively crawls directories starting from 'url'. If a link ends with '/',
    it is assumed to be a directory and is crawled further. Otherwise, if the link
    ends with '.mp3', it is added to the results list.
    """
    print(f"Crawling: {url}")
    html = await fetch(url, session)
    if not html:
        return
    links = await parse_links(html, url)
    tasks = []
    for link in links:
        if link.endswith('/'):
            # Recursively crawl the directory.
            tasks.append(crawl(link, session, results))
        elif link.endswith('.mp3'):
            # Add the mp3 file URL to the results.
            results.append(link)
    if tasks:
        await asyncio.gather(*tasks)

async def main():
    results = []
    async with aiohttp.ClientSession() as session:
        await crawl(BASE_URL, session, results)
    
    # Output the list of MP3 file URLs.
    print("Found MP3 files:")
    print(results)
    
    # Save the resulting list to a JSON file.
    with open('audio-files.json', 'w', encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print("Results saved to audio-files.json")

if __name__ == "__main__":
    asyncio.run(main())
