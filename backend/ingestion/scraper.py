import os
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, raw_dir="backend/data/raw"):
        self.raw_dir = raw_dir
        os.makedirs(self.raw_dir, exist_ok=True)

    def download_url(self, url, filename):
        """
        Download a URL and save it to the raw data directory.
        """
        dest_path = os.path.join(self.raw_dir, filename)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            print(f"Downloading {url} to {dest_path}...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Simple content verification
            if "pdf" in response.headers.get("Content-Type", "").lower() or filename.endswith(".pdf"):
                with open(dest_path, "wb") as f:
                    f.write(response.content)
            else:
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
            print(f"Successfully downloaded {filename}")
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False

if __name__ == "__main__":
    # Example usage / testing
    scraper = Scraper()
    print("Scraper utility initialized.")
