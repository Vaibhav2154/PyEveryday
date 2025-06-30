import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import sys

class NewsFetcher:
    def __init__(self):
        self.sources = {
            'bbc': {
                'url': 'https://www.bbc.com/news',
                'headline_selector': 'h3[class*="gs-c-promo-heading__title"]',
                'link_selector': 'a[class*="gs-c-promo-heading"]'
            },
            'reuters': {
                'url': 'https://www.reuters.com',
                'headline_selector': 'h3[class*="story-title"]',
                'link_selector': 'a[data-testid="Heading"]'
            },
            'hackernews': {
                'url': 'https://news.ycombinator.com',
                'headline_selector': 'a.storylink',
                'link_selector': 'a.storylink'
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_headlines_generic(self, url, max_headlines=10):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = []
            
            title_selectors = [
                'h1', 'h2', 'h3', 'h4',
                '[class*="title"]',
                '[class*="headline"]',
                '[class*="heading"]',
                'a[title]'
            ]
            
            for selector in title_selectors:
                elements = soup.select(selector)
                
                for element in elements[:max_headlines]:
                    text = element.get_text(strip=True)
                    link = element.get('href') or (element.find_parent('a') and element.find_parent('a').get('href'))
                    
                    if text and len(text) > 20:
                        if link and not link.startswith('http'):
                            from urllib.parse import urljoin
                            link = urljoin(url, link)
                        
                        headlines.append({
                            'title': text,
                            'link': link,
                            'source': url
                        })
                
                if len(headlines) >= max_headlines:
                    break
            
            return headlines[:max_headlines]
            
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            return []
    
    def fetch_from_source(self, source_name, max_headlines=10):
        if source_name not in self.sources:
            print(f"Unknown source: {source_name}")
            return []
        
        source = self.sources[source_name]
        
        try:
            response = requests.get(source['url'], headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            if source_name == 'hackernews':
                title_elements = soup.select('a.storylink')
                
                for element in title_elements[:max_headlines]:
                    title = element.get_text(strip=True)
                    link = element.get('href')
                    
                    if not link.startswith('http'):
                        link = f"https://news.ycombinator.com/{link}"
                    
                    headlines.append({
                        'title': title,
                        'link': link,
                        'source': source_name
                    })
            
            else:
                title_elements = soup.select(source['headline_selector'])
                link_elements = soup.select(source['link_selector'])
                
                for i, title_elem in enumerate(title_elements[:max_headlines]):
                    title = title_elem.get_text(strip=True)
                    
                    link = None
                    if i < len(link_elements):
                        link = link_elements[i].get('href')
                    
                    if link and not link.startswith('http'):
                        from urllib.parse import urljoin
                        link = urljoin(source['url'], link)
                    
                    headlines.append({
                        'title': title,
                        'link': link,
                        'source': source_name
                    })
            
            return headlines
            
        except Exception as e:
            print(f"Error fetching from {source_name}: {e}")
            return []
    
    def fetch_all_sources(self, max_per_source=5):
        all_headlines = []
        
        for source_name in self.sources:
            print(f"Fetching from {source_name}...")
            headlines = self.fetch_from_source(source_name, max_per_source)
            all_headlines.extend(headlines)
            time.sleep(1)
        
        return all_headlines
    
    def fetch_custom_source(self, url, max_headlines=10):
        return self.fetch_headlines_generic(url, max_headlines)
    
    def search_news(self, query, max_results=10):
        search_results = []
        
        try:
            google_news_url = f"https://news.google.com/rss/search?q={query}"
            response = requests.get(google_news_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                
                for item in items[:max_results]:
                    title = item.title.get_text() if item.title else "No title"
                    link = item.link.get_text() if item.link else "No link"
                    description = item.description.get_text() if item.description else ""
                    
                    search_results.append({
                        'title': title,
                        'link': link,
                        'description': description,
                        'source': 'Google News'
                    })
        
        except Exception as e:
            print(f"Error searching news: {e}")
        
        return search_results
    
    def display_headlines(self, headlines):
        if not headlines:
            print("No headlines found")
            return
        
        print("\n" + "="*80)
        print("📰 NEWS HEADLINES")
        print("="*80)
        
        for i, headline in enumerate(headlines, 1):
            print(f"\n{i}. {headline['title']}")
            if headline.get('link'):
                print(f"   🔗 {headline['link']}")
            print(f"   📍 Source: {headline.get('source', 'Unknown')}")
            
            if headline.get('description'):
                description = headline['description'][:200] + "..." if len(headline['description']) > 200 else headline['description']
                print(f"   📝 {description}")
            
            print("-" * 80)
    
    def save_headlines(self, headlines, filename=None):
        if not headlines:
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_headlines_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'headlines': headlines
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Headlines saved to {filename}")
    
    def get_trending_topics(self):
        trending = []
        
        try:
            response = requests.get("https://trends.google.com/trends/trendingsearches/daily/rss?geo=US", 
                                  headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                
                for item in items[:10]:
                    title = item.title.get_text() if item.title else "No title"
                    
                    trending.append({
                        'topic': title,
                        'source': 'Google Trends'
                    })
        
        except Exception as e:
            print(f"Error fetching trending topics: {e}")
        
        return trending
    
    def filter_headlines_by_keyword(self, headlines, keywords):
        filtered = []
        keywords = [keyword.lower() for keyword in keywords]
        
        for headline in headlines:
            title_lower = headline['title'].lower()
            if any(keyword in title_lower for keyword in keywords):
                filtered.append(headline)
        
        return filtered

if __name__ == "__main__":
    fetcher = NewsFetcher()
    
    if len(sys.argv) < 2:
        print("Usage: python news_fetcher.py <command> [args]")
        print("Commands:")
        print("  all                    - Fetch from all sources")
        print("  source <name>          - Fetch from specific source (bbc, reuters, hackernews)")
        print("  custom <url>           - Fetch from custom URL")
        print("  search <query>         - Search news")
        print("  trending               - Get trending topics")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "all":
        max_per_source = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        headlines = fetcher.fetch_all_sources(max_per_source)
        fetcher.display_headlines(headlines)
        
        if headlines:
            save = input("\nSave headlines? (y/n): ").lower()
            if save == 'y':
                fetcher.save_headlines(headlines)
    
    elif command == "source":
        if len(sys.argv) < 3:
            print("Available sources: bbc, reuters, hackernews")
            sys.exit(1)
        
        source = sys.argv[2]
        max_headlines = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        headlines = fetcher.fetch_from_source(source, max_headlines)
        fetcher.display_headlines(headlines)
    
    elif command == "custom":
        if len(sys.argv) < 3:
            print("Usage: custom <url>")
            sys.exit(1)
        
        url = sys.argv[2]
        max_headlines = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        headlines = fetcher.fetch_custom_source(url, max_headlines)
        fetcher.display_headlines(headlines)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: search <query>")
            sys.exit(1)
        
        query = " ".join(sys.argv[2:])
        max_results = 10
        headlines = fetcher.search_news(query, max_results)
        fetcher.display_headlines(headlines)
    
    elif command == "trending":
        topics = fetcher.get_trending_topics()
        if topics:
            print("\n🔥 TRENDING TOPICS")
            print("="*40)
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic['topic']}")
        else:
            print("No trending topics found")
    
    else:
        print("Unknown command")
