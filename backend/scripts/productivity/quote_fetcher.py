import random
import requests
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import datetime
import os

console = Console()

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
        self.history = []

    def get_local_quote(self):
        quote = random.choice(self.local_quotes)
        self.history.append(quote)
        return quote

    def get_quote_from_quotable(self):
        try:
            response = requests.get("https://api.quotable.io/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                quote = f"{data['content']} - {data['author']}"
                self.history.append(quote)
                return quote
        except Exception as e:
            pass
        return None

    def get_quote_from_zenquotes(self):
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    quote = f"{data[0]['q']} - {data['a']}"
                    self.history.append(quote)
                    return quote
        except Exception as e:
            pass
        return None

    def get_quote_from_quotegarden(self):
        try:
            response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('statusCode') == 200:
                    quote_data = data['data']
                    quote = f"{quote_data['quoteText']} - {quote_data['quoteAuthor']}"
                    self.history.append(quote)
                    return quote
        except Exception as e:
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
                quote = f"{data['content']} - {data['author']}"
                self.history.append(quote)
                return quote
        except Exception as e:
            pass
        return self.get_local_quote()

    def get_author_quote(self, author):
        try:
            url = f"https://api.quotable.io/random?author={author}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                quote = f"{data['content']} - {data['author']}"
                self.history.append(quote)
                return quote
        except Exception as e:
            pass
        return self.get_local_quote()

    def save_favorite_quote(self, quote, filename="favorite_quotes.txt"):
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"{quote}\n")
            console.print(f"[green]Quote saved to {filename}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving quote: {e}[/red]")

    def get_daily_quote(self):
        today = datetime.date.today()
        random.seed(today.toordinal())
        quote = self.get_random_quote()
        random.seed()
        return quote

    def search_quotes(self, keyword):
        """Search for keyword in local quotes and history."""
        results = [q for q in self.local_quotes + self.history if keyword.lower() in q.lower()]
        return results if results else ["No quotes found with that keyword."]

    def list_favorite_quotes(self, filename="favorite_quotes.txt"):
        if not os.path.exists(filename):
            return ["No favorite quotes saved yet."]
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]


def display_quote_with_formatting(quote):
    console.print(Panel(quote, title="💡 Daily Motivation", subtitle="Powered by Rich", style="bright_magenta"))

def display_search_results(quotes, title="Quote Search Results"):
    table = Table(title=title, box=box.SIMPLE)
    table.add_column("Quote", style="magenta")
    for q in quotes:
        table.add_row(q.strip())
    console.print(table)

def print_usage():
    usage_msg = """
Usage:
    python quote_fetcher.py daily
    python quote_fetcher.py category <category>
    python quote_fetcher.py author <author>
    python quote_fetcher.py save
    python quote_fetcher.py offline
    python quote_fetcher.py search <keyword>
    python quote_fetcher.py favorites
    """
    console.print(Panel(usage_msg, title="HELP", style="bold blue"))

def main():
    fetcher = QuoteFetcher()
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "daily":
            quote = fetcher.get_daily_quote()
            display_quote_with_formatting(quote)
        elif command == "category" and len(sys.argv) > 2:
            category = sys.argv
            quote = fetcher.get_category_quote(category)
            display_quote_with_formatting(quote)
        elif command == "author" and len(sys.argv) > 2:
            author = sys.argv
            quote = fetcher.get_author_quote(author)
            display_quote_with_formatting(quote)
        elif command == "save":
            quote = fetcher.get_random_quote()
            display_quote_with_formatting(quote)
            try:
                save = console.input("Save this quote? (y/n): ").strip().lower()
                if save == 'y':
                    fetcher.save_favorite_quote(quote)
            except Exception:
                console.print("[red]Error reading input[/red]")
        elif command == "offline":
            quote = fetcher.get_local_quote()
            display_quote_with_formatting(quote)
        elif command == "search" and len(sys.argv) > 2:
            keyword = sys.argv[2]
            results = fetcher.search_quotes(keyword)
            display_search_results(results)
        elif command == "favorites":
            favs = fetcher.list_favorite_quotes()
            display_search_results(favs, title="Favorite Quotes")
        else:
            print_usage()
    else:
        quote = fetcher.get_random_quote()
        display_quote_with_formatting(quote)

if __name__ == "__main__":
    main()
