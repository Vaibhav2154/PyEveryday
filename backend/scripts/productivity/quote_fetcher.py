import random
import requests
import json

class QuoteFetcher:
    def __init__(self):
        self.local_quotes = [
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty. - Winston Churchill",
            "Don't let yesterday take up too much of today. - Will Rogers",
            "You learn more from failure than from success. - Unknown",
            "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
            "If you are working on something that you really care about, you don't have to be pushed. The vision pulls you. - Steve Jobs",
            "People who are crazy enough to think they can change the world, are the ones who do. - Rob Siltanen",
            "Failure will never overtake me if my determination to succeed is strong enough. - Og Mandino",
            "Entrepreneurs are great at dealing with uncertainty and also very good at minimizing risk. - Mohnish Pabrai",
            "We don't make mistakes, just happy little accidents. - Bob Ross"
        ]
        
        self.api_urls = [
            "https://api.quotable.io/random",
            "https://zenquotes.io/api/random",
            "https://quote-garden.herokuapp.com/api/v3/quotes/random"
        ]
    
    def get_local_quote(self):
        return random.choice(self.local_quotes)
    
    def get_quote_from_quotable(self):
        try:
            response = requests.get("https://api.quotable.io/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"{data['content']} - {data['author']}"
        except:
            pass
        return None
    
    def get_quote_from_zenquotes(self):
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return f"{data[0]['q']} - {data[0]['a']}"
        except:
            pass
        return None
    
    def get_quote_from_quotegarden(self):
        try:
            response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['statusCode'] == 200:
                    quote_data = data['data']
                    return f"{quote_data['quoteText']} - {quote_data['quoteAuthor']}"
        except:
            pass
        return None
    
    def get_random_quote(self, prefer_online=True):
        if prefer_online:
            methods = [
                self.get_quote_from_quotable,
                self.get_quote_from_zenquotes,
                self.get_quote_from_quotegarden
            ]
            
            random.shuffle(methods)
            
            for method in methods:
                quote = method()
                if quote:
                    return quote
        
        return self.get_local_quote()
    
    def get_category_quote(self, category="motivational"):
        try:
            url = f"https://api.quotable.io/random?tags={category}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"{data['content']} - {data['author']}"
        except:
            pass
        
        return self.get_local_quote()
    
    def get_author_quote(self, author):
        try:
            url = f"https://api.quotable.io/random?author={author}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"{data['content']} - {data['author']}"
        except:
            pass
        
        return self.get_local_quote()
    
    def save_favorite_quote(self, quote, filename="favorite_quotes.txt"):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{quote}\n")
        print(f"Quote saved to {filename}")
    
    def get_daily_quote(self):
        import datetime
        today = datetime.date.today()
        random.seed(today.toordinal())
        
        quote = self.get_random_quote()
        random.seed()
        return quote

def display_quote_with_formatting(quote):
    print("\n" + "="*60)
    print("💡 DAILY MOTIVATION")
    print("="*60)
    print(f"\n{quote}\n")
    print("="*60)

if __name__ == "__main__":
    import sys
    
    fetcher = QuoteFetcher()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "daily":
            quote = fetcher.get_daily_quote()
            display_quote_with_formatting(quote)
        
        elif command == "category" and len(sys.argv) > 2:
            category = sys.argv[2]
            quote = fetcher.get_category_quote(category)
            display_quote_with_formatting(quote)
        
        elif command == "author" and len(sys.argv) > 2:
            author = sys.argv[2]
            quote = fetcher.get_author_quote(author)
            display_quote_with_formatting(quote)
        
        elif command == "save":
            quote = fetcher.get_random_quote()
            display_quote_with_formatting(quote)
            save = input("Save this quote? (y/n): ").lower()
            if save == 'y':
                fetcher.save_favorite_quote(quote)
        
        elif command == "offline":
            quote = fetcher.get_local_quote()
            display_quote_with_formatting(quote)
        
        else:
            print("Usage: python quote_fetcher.py [daily|category <cat>|author <name>|save|offline]")
    
    else:
        quote = fetcher.get_random_quote()
        display_quote_with_formatting(quote)
