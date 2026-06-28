from collections import deque
from urllib.parse import urlparse

from scraper import PageScraper


class WebsiteCrawler:
    """
    Breadth-First Search (BFS) website crawler.
    """

    def __init__(self, start_url, max_pages=25):

        self.start_url = start_url
        self.max_pages = max_pages

        self.scraper = PageScraper()

        self.queue = deque()
        self.visited = set()
        self.pages = []

        self.base_domain = urlparse(start_url).netloc

        # Restrict crawling to agriculture-related pages.
        self.allowed_paths = [
            "/themes/economy/agriculture",
            "/documents"
        ]

    def is_allowed_url(self, url):

        parsed = urlparse(url)

        if parsed.netloc != self.base_domain:
            return False

        for path in self.allowed_paths:
            if parsed.path.startswith(path):
                return True

        return False

    def crawl(self):
        """
        Crawl the website using Breadth-First Search.

        Returns
        -------
        list
            List of scraped page dictionaries.
        """

        self.queue.append(self.start_url)

        while self.queue and len(self.pages) < self.max_pages:

            url = self.queue.popleft()

            if url in self.visited:
                continue

            self.visited.add(url)

            print(f"Crawling: {url}")

            page = self.scraper.scrape(url)

            if page is None:
                continue

            self.pages.append(page)

            for link in page["links"]:

                if link in self.visited:
                    continue

                if not self.is_allowed_url(link):
                    continue

                if link not in self.queue:
                    self.queue.append(link)

        print(f"\nCompleted. Pages Crawled: {len(self.pages)}")

        return self.pages
