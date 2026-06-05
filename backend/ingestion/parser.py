import os
import re
from bs4 import BeautifulSoup
import pdfplumber

class Parser:
    def __init__(self, raw_dir="backend/data/raw"):
        self.raw_dir = raw_dir

    def map_scheme(self, filename, title_text=""):
        """
        Map a filename or parsed title to one of the 6 scoped schemes or 'General'.
        """
        text = (filename + " " + title_text).lower()
        if "contra" in text:
            return "SBI Contra Fund"
        elif "elss" in text or "long_term" in text or "tax_saver" in text:
            return "SBI Long Term Equity Fund"
        elif "flexicap" in text:
            return "SBI Flexicap Fund"
        elif "large_cap" in text or "bluechip" in text:
            return "SBI Bluechip Fund"
        elif "liquid" in text:
            return "SBI Liquid Fund"
        elif "small_cap" in text:
            return "SBI Small Cap Fund"
        elif "statement" in text or "faq" in text:
            return "General"
        return "General"

    def parse_html(self, file_path):
        """
        Parse raw HTML factsheet/FAQ files.
        """
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        
        # 1. Target main content block to avoid boilerplate
        content_div = soup.find(id="content")
        if not content_div:
            content_div = soup.find("body") or soup

        # 2. Extract metadata from markup
        source_url = ""
        date_accessed = "June 1, 2026"  # Default fallback
        
        # Search for metadata in paragraphs
        for p in content_div.find_all("p"):
            text_val = p.get_text()
            if "Source URL:" in text_val:
                if p.find("a"):
                    source_url = p.find("a")["href"]
                else:
                    source_url = text_val.replace("Source URL:", "").strip()
            elif "As on:" in text_val:
                date_accessed = text_val.replace("As on:", "").strip()

        # Clean text: remove script and style elements
        for script_or_style in content_div(["script", "style"]):
            script_or_style.decompose()
            
        # Get raw clean text
        text = content_div.get_text(separator="\n")
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for phrase in lines if phrase.strip())
        clean_text = "\n".join(chunks)

        title = soup.title.string.strip() if soup.title else filename
        scheme_name = self.map_scheme(filename, title)
        doc_type = "faq" if "statement" in filename or "faq" in filename else "factsheet"

        return {
            "text": clean_text,
            "metadata": {
                "source_url": source_url,
                "scheme_name": scheme_name,
                "document_type": doc_type,
                "date_accessed": date_accessed,
                "title": title,
                "filename": filename
            }
        }

    def parse_pdf(self, file_path):
        """
        Parse raw PDF files using pdfplumber.
        """
        filename = os.path.basename(file_path)
        clean_text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    clean_text += text + "\n"

        scheme_name = self.map_scheme(filename)
        doc_type = "pdf"
        
        return {
            "text": clean_text.strip(),
            "metadata": {
                "source_url": "",  # Default fallback
                "scheme_name": scheme_name,
                "document_type": doc_type,
                "date_accessed": "June 1, 2026",
                "title": filename,
                "filename": filename
            }
        }

    def parse_all(self):
        """
        Parse all files under raw_dir.
        """
        parsed_docs = []
        if not os.path.exists(self.raw_dir):
            print(f"Directory {self.raw_dir} does not exist!")
            return parsed_docs

        for f in os.listdir(self.raw_dir):
            path = os.path.join(self.raw_dir, f)
            if os.path.isdir(path) or f.startswith("."):
                continue

            print(f"Parsing {f}...")
            if f.endswith(".html") or f.endswith(".htm"):
                doc = self.parse_html(path)
                parsed_docs.append(doc)
            elif f.endswith(".pdf"):
                doc = self.parse_pdf(path)
                parsed_docs.append(doc)
            else:
                print(f"Skipping unsupported file type: {f}")

        return parsed_docs

if __name__ == "__main__":
    parser = Parser()
    docs = parser.parse_all()
    print(f"Parsed {len(docs)} documents.")
    if docs:
        print(f"First doc metadata: {docs[0]['metadata']}")
