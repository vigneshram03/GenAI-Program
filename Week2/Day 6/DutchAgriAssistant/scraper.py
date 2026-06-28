import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class PageScraper:
    """
    Scrapes a single web page and returns:
    {
        "title": "...",
        "url": "...",
        "text": "...",
        "links": [...]
    }
    """

    def __init__(self):

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0 Safari/537.36"
            )
        }

        self.remove_tags = [
            "script",
            "style",
            "header",
            "footer",
            "nav",
            "noscript",
            "svg",
            "iframe",
            "form",
            "aside"
        ]

        self.content_tags = [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "li"
        ]

        self.ignore_extensions = (
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".svg",
            ".zip",
            ".rar",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".mp4",
            ".mp3"
        )

    # ---------------------------------------------------------

    def download_page(self, url):

        response = requests.get(
            url,
            headers=self.headers,
            timeout=20
        )

        response.raise_for_status()

        return response.text

    # ---------------------------------------------------------

    def clean_html(self, soup):

        for tag in soup(self.remove_tags):
            tag.decompose()

        return soup

    # ---------------------------------------------------------

    def extract_title(self, soup):

        h1 = soup.find("h1")

        if h1:
            return h1.get_text(strip=True)

        if soup.title:
            return soup.title.get_text(strip=True)

        return "No Title"

    # ---------------------------------------------------------

    def extract_text(self, soup):

        content = []

        for tag in soup.find_all(self.content_tags):

            text = tag.get_text(" ", strip=True)

            if len(text) < 20:
                continue

            content.append(text)

        return "\n\n".join(content)

    # ---------------------------------------------------------

    def extract_links(self, soup, current_url):

        links = []

        base_domain = urlparse(current_url).netloc

        for link in soup.find_all("a", href=True):

            href = urljoin(current_url, link["href"])

            href = href.split("#")[0].strip()

            if not href:
                continue

            parsed = urlparse(href)

            if parsed.netloc != base_domain:
                continue

            if href.startswith(("mailto:", "javascript:")):
                continue

            if href.lower().endswith(self.ignore_extensions):
                continue

            if href not in links:
                links.append(href)

        return links

    # ---------------------------------------------------------

    def scrape(self, url):

        try:

            html = self.download_page(url)

            soup = BeautifulSoup(html, "html.parser")

            soup = self.clean_html(soup)

            return {
                "title": self.extract_title(soup),
                "url": url,
                "text": self.extract_text(soup),
                "links": self.extract_links(soup, url)
            }

        except Exception as ex:

            print(f"Failed to scrape: {url}")
            print(ex)

            return None
