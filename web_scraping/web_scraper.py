import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import sys
from urllib.parse import urljoin, urlparse
import re

class WebScraper:
    def __init__(self, delay=1):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_page(self, url, timeout=10):
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def scrape_text(self, url, selectors=None):
        response = self.get_page(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if selectors:
            extracted_data = {}
            for name, selector in selectors.items():
                elements = soup.select(selector)
                extracted_data[name] = [elem.get_text(strip=True) for elem in elements]
            return extracted_data
        else:
            return soup.get_text(strip=True)
    
    def scrape_links(self, url, filter_pattern=None, absolute=True):
        response = self.get_page(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            if absolute and not href.startswith('http'):
                href = urljoin(url, href)
            
            if filter_pattern:
                if re.search(filter_pattern, href):
                    links.append({
                        'url': href,
                        'text': link.get_text(strip=True),
                        'title': link.get('title', '')
                    })
            else:
                links.append({
                    'url': href,
                    'text': link.get_text(strip=True),
                    'title': link.get('title', '')
                })
        
        return links
    
    def scrape_images(self, url, min_size=None):
        response = self.get_page(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if not src:
                continue
            
            if not src.startswith('http'):
                src = urljoin(url, src)
            
            alt_text = img.get('alt', '')
            title = img.get('title', '')
            
            image_data = {
                'url': src,
                'alt': alt_text,
                'title': title,
                'width': img.get('width'),
                'height': img.get('height')
            }
            
            images.append(image_data)
        
        return images
    
    def scrape_table(self, url, table_selector='table'):
        response = self.get_page(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.select(table_selector)
        
        if not tables:
            return None
        
        table_data = []
        
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue
            
            headers = []
            header_row = rows[0]
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.get_text(strip=True))
            
            table_rows = []
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                row_data = []
                for cell in cells:
                    row_data.append(cell.get_text(strip=True))
                if row_data:
                    table_rows.append(row_data)
            
            table_data.append({
                'headers': headers,
                'rows': table_rows
            })
        
        return table_data
    
    def scrape_forms(self, url):
        response = self.get_page(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'fields': []
            }
            
            for input_field in form.find_all(['input', 'select', 'textarea']):
                field_data = {
                    'type': input_field.get('type', input_field.name),
                    'name': input_field.get('name', ''),
                    'id': input_field.get('id', ''),
                    'required': input_field.get('required') is not None,
                    'placeholder': input_field.get('placeholder', '')
                }
                
                if input_field.name == 'select':
                    options = [option.get_text(strip=True) for option in input_field.find_all('option')]
                    field_data['options'] = options
                
                form_data['fields'].append(field_data)
            
            forms.append(form_data)
        
        return forms
    
    def scrape_multiple_pages(self, urls, selectors, output_format='json'):
        all_data = []
        
        for i, url in enumerate(urls):
            print(f"Scraping {i+1}/{len(urls)}: {url}")
            
            data = self.scrape_text(url, selectors)
            if data:
                data['source_url'] = url
                all_data.append(data)
            
            if i < len(urls) - 1:
                time.sleep(self.delay)
        
        return all_data
    
    def follow_pagination(self, start_url, next_selector, max_pages=10, data_selectors=None):
        all_data = []
        current_url = start_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            print(f"Scraping page {page_count + 1}: {current_url}")
            
            response = self.get_page(current_url)
            if not response:
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if data_selectors:
                page_data = {}
                for name, selector in data_selectors.items():
                    elements = soup.select(selector)
                    page_data[name] = [elem.get_text(strip=True) for elem in elements]
                page_data['page_number'] = page_count + 1
                page_data['source_url'] = current_url
                all_data.append(page_data)
            
            next_link = soup.select_one(next_selector)
            if next_link and next_link.get('href'):
                current_url = urljoin(current_url, next_link['href'])
                page_count += 1
                time.sleep(self.delay)
            else:
                break
        
        return all_data
    
    def save_data(self, data, filename, format='json'):
        if format.lower() == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif format.lower() == 'csv':
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], dict):
                    fieldnames = data[0].keys()
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(data)
                else:
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        for row in data:
                            writer.writerow([row] if not isinstance(row, list) else row)
        
        elif format.lower() == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, list):
                    for item in data:
                        f.write(str(item) + '\n')
                else:
                    f.write(str(data))
        
        print(f"Data saved to {filename}")
    
    def get_page_metadata(self, url):
        response = self.get_page(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        metadata = {
            'title': soup.title.string if soup.title else '',
            'description': '',
            'keywords': '',
            'author': '',
            'canonical_url': '',
            'lang': soup.html.get('lang', '') if soup.html else '',
            'charset': 'utf-8'
        }
        
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            property_name = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description' or property_name == 'og:description':
                metadata['description'] = content
            elif name == 'keywords':
                metadata['keywords'] = content
            elif name == 'author':
                metadata['author'] = content
            elif meta.get('charset'):
                metadata['charset'] = meta.get('charset')
        
        canonical = soup.find('link', rel='canonical')
        if canonical:
            metadata['canonical_url'] = canonical.get('href', '')
        
        return metadata

def create_sample_config():
    sample_config = {
        "urls": [
            "https://example.com/page1",
            "https://example.com/page2"
        ],
        "selectors": {
            "titles": "h1, h2",
            "paragraphs": "p",
            "links": "a"
        },
        "output": {
            "format": "json",
            "filename": "scraped_data.json"
        },
        "settings": {
            "delay": 1,
            "timeout": 10
        }
    }
    
    with open('scraper_config.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    print("Sample configuration created: scraper_config.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_scraper.py <command> [args]")
        print("Commands:")
        print("  text <url> [selectors_json]     - Scrape text content")
        print("  links <url> [pattern]           - Scrape links")
        print("  images <url>                    - Scrape images")
        print("  table <url> [selector]          - Scrape tables")
        print("  forms <url>                     - Scrape forms")
        print("  metadata <url>                  - Get page metadata")
        print("  config                          - Create sample config")
        sys.exit(1)
    
    command = sys.argv[1]
    scraper = WebScraper()
    
    if command == "text":
        if len(sys.argv) < 3:
            print("Usage: text <url> [selectors_json]")
            sys.exit(1)
        
        url = sys.argv[2]
        selectors = None
        
        if len(sys.argv) > 3:
            try:
                selectors = json.loads(sys.argv[3])
            except json.JSONDecodeError:
                print("Invalid JSON for selectors")
                sys.exit(1)
        
        data = scraper.scrape_text(url, selectors)
        if data:
            print(json.dumps(data, indent=2, ensure_ascii=False))
    
    elif command == "links":
        if len(sys.argv) < 3:
            print("Usage: links <url> [pattern]")
            sys.exit(1)
        
        url = sys.argv[2]
        pattern = sys.argv[3] if len(sys.argv) > 3 else None
        
        links = scraper.scrape_links(url, pattern)
        for link in links[:20]:
            print(f"URL: {link['url']}")
            print(f"Text: {link['text']}")
            print("-" * 50)
    
    elif command == "images":
        if len(sys.argv) < 3:
            print("Usage: images <url>")
            sys.exit(1)
        
        url = sys.argv[2]
        images = scraper.scrape_images(url)
        
        for img in images[:10]:
            print(f"URL: {img['url']}")
            print(f"Alt: {img['alt']}")
            print(f"Size: {img['width']}x{img['height']}")
            print("-" * 50)
    
    elif command == "table":
        if len(sys.argv) < 3:
            print("Usage: table <url> [selector]")
            sys.exit(1)
        
        url = sys.argv[2]
        selector = sys.argv[3] if len(sys.argv) > 3 else 'table'
        
        tables = scraper.scrape_table(url, selector)
        if tables:
            for i, table in enumerate(tables):
                print(f"Table {i+1}:")
                print("Headers:", table['headers'])
                print("Rows:", len(table['rows']))
                if table['rows']:
                    print("Sample row:", table['rows'][0])
                print("-" * 50)
    
    elif command == "forms":
        if len(sys.argv) < 3:
            print("Usage: forms <url>")
            sys.exit(1)
        
        url = sys.argv[2]
        forms = scraper.scrape_forms(url)
        
        for i, form in enumerate(forms):
            print(f"Form {i+1}:")
            print(f"Action: {form['action']}")
            print(f"Method: {form['method']}")
            print(f"Fields: {len(form['fields'])}")
            for field in form['fields'][:5]:
                print(f"  - {field['type']}: {field['name']}")
            print("-" * 50)
    
    elif command == "metadata":
        if len(sys.argv) < 3:
            print("Usage: metadata <url>")
            sys.exit(1)
        
        url = sys.argv[2]
        metadata = scraper.get_page_metadata(url)
        
        if metadata:
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
    
    elif command == "config":
        create_sample_config()
    
    else:
        print("Unknown command")
