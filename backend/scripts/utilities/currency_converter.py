import requests
import json
import sys
from datetime import datetime

class CurrencyConverter:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        self.fallback_url = "https://api.fixer.io/latest"
        
        self.common_currencies = {
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'JPY': 'Japanese Yen',
            'CAD': 'Canadian Dollar',
            'AUD': 'Australian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'INR': 'Indian Rupee',
            'KRW': 'South Korean Won',
            'MXN': 'Mexican Peso',
            'BRL': 'Brazilian Real',
            'RUB': 'Russian Ruble',
            'ZAR': 'South African Rand',
            'SGD': 'Singapore Dollar'
        }
    
    def get_exchange_rates(self, base_currency='USD'):
        try:
            url = f"{self.base_url}/{base_currency.upper()}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('rates', {})
        
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return self.get_fallback_rates(base_currency)
    
    def get_fallback_rates(self, base_currency='USD'):
        try:
            params = {'base': base_currency.upper()}
            if self.api_key:
                params['access_key'] = self.api_key
            
            response = requests.get(self.fallback_url, params=params, timeout=10)
            data = response.json()
            
            if data.get('success'):
                return data.get('rates', {})
        except:
            pass
        
        return self.get_offline_rates()
    
    def get_offline_rates(self):
        return {
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.0,
            'CAD': 1.25,
            'AUD': 1.35,
            'CHF': 0.92,
            'CNY': 6.45,
            'INR': 74.5,
            'KRW': 1180.0,
            'MXN': 20.1,
            'BRL': 5.2,
            'RUB': 73.5,
            'ZAR': 14.8,
            'SGD': 1.35
        }
    
    def convert(self, amount, from_currency, to_currency):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency == to_currency:
            return amount
        
        if from_currency == 'USD':
            rates = self.get_exchange_rates('USD')
            if to_currency in rates:
                return amount * rates[to_currency]
        
        elif to_currency == 'USD':
            rates = self.get_exchange_rates('USD')
            if from_currency in rates:
                return amount / rates[from_currency]
        
        else:
            usd_rates = self.get_exchange_rates('USD')
            if from_currency in usd_rates and to_currency in usd_rates:
                usd_amount = amount / usd_rates[from_currency]
                return usd_amount * usd_rates[to_currency]
        
        print(f"Conversion not available for {from_currency} to {to_currency}")
        return None
    
    def get_currency_info(self, currency_code):
        currency_code = currency_code.upper()
        return self.common_currencies.get(currency_code, 'Unknown Currency')
    
    def list_supported_currencies(self):
        rates = self.get_exchange_rates()
        return list(rates.keys())
    
    def get_historical_rate(self, date, from_currency, to_currency):
        try:
            url = f"https://api.exchangerate-api.com/v4/history/{from_currency.upper()}/{date}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'rates' in data and to_currency.upper() in data['rates']:
                return data['rates'][to_currency.upper()]
        except:
            pass
        
        return None
    
    def calculate_percentage_change(self, old_rate, new_rate):
        if old_rate and new_rate:
            change = ((new_rate - old_rate) / old_rate) * 100
            return round(change, 2)
        return None
    
    def format_currency(self, amount, currency):
        currency = currency.upper()
        
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
            'KRW': '₩'
        }
        
        symbol = currency_symbols.get(currency, currency)
        
        if currency in ['JPY', 'KRW']:
            return f"{symbol}{amount:,.0f}"
        else:
            return f"{symbol}{amount:,.2f}"
    
    def convert_and_display(self, amount, from_currency, to_currency):
        result = self.convert(amount, from_currency, to_currency)
        
        if result is not None:
            from_formatted = self.format_currency(amount, from_currency)
            to_formatted = self.format_currency(result, to_currency)
            
            from_name = self.get_currency_info(from_currency)
            to_name = self.get_currency_info(to_currency)
            
            print(f"\n💱 CURRENCY CONVERSION")
            print("="*40)
            print(f"From: {from_formatted} ({from_name})")
            print(f"To:   {to_formatted} ({to_name})")
            print(f"Rate: 1 {from_currency} = {result/amount:.4f} {to_currency}")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*40)
            
            return result
        else:
            print("Conversion failed")
            return None
    
    def compare_multiple_currencies(self, amount, base_currency, target_currencies):
        print(f"\n💰 CURRENCY COMPARISON")
        print(f"Base Amount: {self.format_currency(amount, base_currency)}")
        print("="*50)
        
        for currency in target_currencies:
            result = self.convert(amount, base_currency, currency)
            if result:
                formatted = self.format_currency(result, currency)
                name = self.get_currency_info(currency)
                print(f"{currency}: {formatted} ({name})")
        
        print("="*50)
    
    def save_conversion_history(self, conversion_data, filename="conversion_history.json"):
        try:
            with open(filename, 'r') as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
        
        history.append(conversion_data)
        
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)

if __name__ == "__main__":
    converter = CurrencyConverter()
    
    if len(sys.argv) < 2:
        print("Usage: python currency_converter.py <command> [args]")
        print("Commands:")
        print("  convert <amount> <from> <to>           - Convert currency")
        print("  compare <amount> <base> <cur1,cur2>    - Compare multiple currencies")
        print("  list                                   - List supported currencies")
        print("  info <currency>                        - Get currency information")
        print("  rates <base>                           - Get all rates for base currency")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "convert":
        if len(sys.argv) < 5:
            print("Usage: convert <amount> <from_currency> <to_currency>")
            sys.exit(1)
        
        try:
            amount = float(sys.argv[2])
            from_currency = sys.argv[3]
            to_currency = sys.argv[4]
            
            result = converter.convert_and_display(amount, from_currency, to_currency)
            
            if result:
                conversion_data = {
                    'timestamp': datetime.now().isoformat(),
                    'amount': amount,
                    'from_currency': from_currency.upper(),
                    'to_currency': to_currency.upper(),
                    'result': result,
                    'rate': result / amount
                }
                converter.save_conversion_history(conversion_data)
        
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    elif command == "compare":
        if len(sys.argv) < 5:
            print("Usage: compare <amount> <base_currency> <currency1,currency2,currency3>")
            sys.exit(1)
        
        try:
            amount = float(sys.argv[2])
            base_currency = sys.argv[3]
            target_currencies = [c.strip() for c in sys.argv[4].split(',')]
            
            converter.compare_multiple_currencies(amount, base_currency, target_currencies)
        
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    elif command == "list":
        currencies = converter.list_supported_currencies()
        print("\nSupported Currencies:")
        print("="*30)
        
        for currency in sorted(currencies)[:20]:
            name = converter.get_currency_info(currency)
            print(f"{currency}: {name}")
        
        print(f"\n... and {len(currencies)-20} more currencies")
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: info <currency_code>")
            sys.exit(1)
        
        currency = sys.argv[2]
        info = converter.get_currency_info(currency)
        print(f"\n{currency.upper()}: {info}")
    
    elif command == "rates":
        if len(sys.argv) < 3:
            print("Usage: rates <base_currency>")
            sys.exit(1)
        
        base = sys.argv[2]
        rates = converter.get_exchange_rates(base)
        
        print(f"\nExchange rates for {base.upper()}:")
        print("="*30)
        
        for currency, rate in sorted(rates.items())[:15]:
            name = converter.get_currency_info(currency)
            print(f"1 {base.upper()} = {rate:.4f} {currency} ({name})")
    
    else:
        print("Unknown command")
