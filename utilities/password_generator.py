import random
import string
import secrets
import sys
import json
import hashlib

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1lI"
        
        self.word_lists = {
            'colors': ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'black', 'white', 'gray'],
            'animals': ['cat', 'dog', 'bird', 'fish', 'lion', 'tiger', 'bear', 'wolf', 'fox', 'deer'],
            'objects': ['book', 'chair', 'table', 'phone', 'computer', 'car', 'house', 'tree', 'flower', 'star']
        }
    
    def generate_random_password(self, length=12, include_uppercase=True, include_lowercase=True, 
                                include_digits=True, include_symbols=True, exclude_ambiguous=False):
        if length < 4:
            raise ValueError("Password length must be at least 4")
        
        characters = ""
        required_chars = []
        
        if include_lowercase:
            characters += self.lowercase
            if exclude_ambiguous:
                characters = ''.join(c for c in characters if c not in self.ambiguous)
            required_chars.append(secrets.choice(self.lowercase))
        
        if include_uppercase:
            characters += self.uppercase
            if exclude_ambiguous:
                characters = ''.join(c for c in characters if c not in self.ambiguous)
            required_chars.append(secrets.choice(self.uppercase))
        
        if include_digits:
            digits = self.digits
            if exclude_ambiguous:
                digits = ''.join(c for c in digits if c not in self.ambiguous)
            characters += digits
            required_chars.append(secrets.choice(digits))
        
        if include_symbols:
            characters += self.symbols
            required_chars.append(secrets.choice(self.symbols))
        
        if not characters:
            raise ValueError("At least one character type must be included")
        
        password_chars = required_chars[:]
        
        for _ in range(length - len(required_chars)):
            password_chars.append(secrets.choice(characters))
        
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_memorable_password(self, num_words=3, separator='-', include_numbers=True, capitalize=True):
        words = []
        
        for _ in range(num_words):
            category = secrets.choice(list(self.word_lists.keys()))
            word = secrets.choice(self.word_lists[category])
            
            if capitalize:
                word = word.capitalize()
            
            words.append(word)
        
        password = separator.join(words)
        
        if include_numbers:
            numbers = ''.join([str(secrets.randbelow(10)) for _ in range(2)])
            password += numbers
        
        return password
    
    def generate_passphrase(self, num_words=4, min_length=6, max_length=12):
        word_pool = []
        for word_list in self.word_lists.values():
            word_pool.extend([word for word in word_list if min_length <= len(word) <= max_length])
        
        if len(word_pool) < num_words:
            word_pool = ['word', 'pass', 'secure', 'random', 'crypto', 'safety']
        
        selected_words = []
        for _ in range(num_words):
            word = secrets.choice(word_pool)
            selected_words.append(word.capitalize())
        
        return ' '.join(selected_words)
    
    def generate_pin(self, length=4):
        if length < 1:
            raise ValueError("PIN length must be at least 1")
        
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
    
    def generate_hex_password(self, length=16):
        if length < 4:
            raise ValueError("Hex password length must be at least 4")
        
        hex_chars = '0123456789abcdef'
        return ''.join([secrets.choice(hex_chars) for _ in range(length)])
    
    def check_password_strength(self, password):
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Use at least 8 characters")
        
        if len(password) >= 12:
            score += 1
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Include lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Include uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Include numbers")
        
        if any(c in self.symbols for c in password):
            score += 1
        else:
            feedback.append("Include special characters")
        
        if len(set(password)) > len(password) * 0.7:
            score += 1
        else:
            feedback.append("Avoid too many repeated characters")
        
        if not any(password[i:i+3] in common_patterns for i in range(len(password)-2)
                  for common_patterns in ['123', 'abc', 'qwe', 'password', 'admin']):
            score += 1
        else:
            feedback.append("Avoid common patterns")
        
        strength_levels = {
            0: "Very Weak",
            1: "Very Weak", 
            2: "Weak",
            3: "Fair",
            4: "Good",
            5: "Strong",
            6: "Very Strong",
            7: "Excellent",
            8: "Excellent"
        }
        
        strength = strength_levels.get(score, "Unknown")
        
        return {
            'score': score,
            'max_score': 8,
            'strength': strength,
            'feedback': feedback,
            'length': len(password),
            'unique_chars': len(set(password))
        }
    
    def generate_multiple_passwords(self, count=5, **kwargs):
        passwords = []
        for _ in range(count):
            password = self.generate_random_password(**kwargs)
            strength = self.check_password_strength(password)
            passwords.append({
                'password': password,
                'strength': strength['strength'],
                'score': strength['score']
            })
        
        passwords.sort(key=lambda x: x['score'], reverse=True)
        return passwords
    
    def save_passwords(self, passwords, filename="generated_passwords.json"):
        data = {
            'generated_at': str(secrets.token_hex(8)),
            'passwords': passwords
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Passwords saved to {filename}")
    
    def generate_custom_pattern(self, pattern):
        result = ""
        
        for char in pattern:
            if char == 'L':
                result += secrets.choice(self.lowercase)
            elif char == 'U':
                result += secrets.choice(self.uppercase)
            elif char == 'D':
                result += secrets.choice(self.digits)
            elif char == 'S':
                result += secrets.choice(self.symbols)
            elif char == 'X':
                all_chars = self.lowercase + self.uppercase + self.digits
                result += secrets.choice(all_chars)
            else:
                result += char
        
        return result
    
    def display_password_info(self, password, show_strength=True):
        print(f"\n🔐 Generated Password: {password}")
        
        if show_strength:
            strength = self.check_password_strength(password)
            print(f"📊 Strength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
            print(f"📏 Length: {strength['length']} characters")
            print(f"🔤 Unique characters: {strength['unique_chars']}")
            
            if strength['feedback']:
                print("💡 Suggestions:")
                for suggestion in strength['feedback']:
                    print(f"   - {suggestion}")
        
        print("="*50)

def create_password_config():
    config = {
        "default_length": 12,
        "include_uppercase": True,
        "include_lowercase": True,
        "include_digits": True,
        "include_symbols": True,
        "exclude_ambiguous": False,
        "memorable_words": 3,
        "memorable_separator": "-",
        "pin_length": 4
    }
    
    with open('password_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("Password configuration created: password_config.json")

if __name__ == "__main__":
    generator = PasswordGenerator()
    
    if len(sys.argv) < 2:
        print("Usage: python password_generator.py <command> [args]")
        print("Commands:")
        print("  random [length] [options]          - Generate random password")
        print("  memorable [words] [separator]      - Generate memorable password")
        print("  passphrase [words]                 - Generate passphrase")
        print("  pin [length]                       - Generate PIN")
        print("  hex [length]                       - Generate hex password")
        print("  multiple [count] [length]          - Generate multiple passwords")
        print("  check <password>                   - Check password strength")
        print("  pattern <pattern>                  - Generate from pattern (L=lower, U=upper, D=digit, S=symbol)")
        print("  config                             - Create configuration file")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "random":
            length = int(sys.argv[2]) if len(sys.argv) > 2 else 12
            
            options = {
                'include_uppercase': '--no-upper' not in sys.argv,
                'include_lowercase': '--no-lower' not in sys.argv,
                'include_digits': '--no-digits' not in sys.argv,
                'include_symbols': '--no-symbols' not in sys.argv,
                'exclude_ambiguous': '--no-ambiguous' in sys.argv
            }
            
            password = generator.generate_random_password(length, **options)
            generator.display_password_info(password)
        
        elif command == "memorable":
            words = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            separator = sys.argv[3] if len(sys.argv) > 3 else '-'
            
            password = generator.generate_memorable_password(words, separator)
            generator.display_password_info(password)
        
        elif command == "passphrase":
            words = int(sys.argv[2]) if len(sys.argv) > 2 else 4
            
            password = generator.generate_passphrase(words)
            generator.display_password_info(password, show_strength=False)
        
        elif command == "pin":
            length = int(sys.argv[2]) if len(sys.argv) > 2 else 4
            
            pin = generator.generate_pin(length)
            print(f"\n🔢 Generated PIN: {pin}")
            print("="*30)
        
        elif command == "hex":
            length = int(sys.argv[2]) if len(sys.argv) > 2 else 16
            
            password = generator.generate_hex_password(length)
            print(f"\n🔣 Generated Hex Password: {password}")
            print("="*40)
        
        elif command == "multiple":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            length = int(sys.argv[3]) if len(sys.argv) > 3 else 12
            
            passwords = generator.generate_multiple_passwords(count, length=length)
            
            print(f"\n🔐 {count} GENERATED PASSWORDS")
            print("="*50)
            
            for i, pwd_data in enumerate(passwords, 1):
                print(f"{i}. {pwd_data['password']}")
                print(f"   Strength: {pwd_data['strength']} ({pwd_data['score']}/8)")
                print()
            
            save = input("Save passwords to file? (y/n): ").lower()
            if save == 'y':
                generator.save_passwords(passwords)
        
        elif command == "check":
            if len(sys.argv) < 3:
                print("Usage: check <password>")
                sys.exit(1)
            
            password = sys.argv[2]
            strength = generator.check_password_strength(password)
            
            print(f"\n🔍 PASSWORD STRENGTH ANALYSIS")
            print("="*40)
            print(f"Password: {password}")
            print(f"Strength: {strength['strength']}")
            print(f"Score: {strength['score']}/{strength['max_score']}")
            print(f"Length: {strength['length']} characters")
            print(f"Unique characters: {strength['unique_chars']}")
            
            if strength['feedback']:
                print("\n💡 Improvement suggestions:")
                for suggestion in strength['feedback']:
                    print(f"   - {suggestion}")
            
            print("="*40)
        
        elif command == "pattern":
            if len(sys.argv) < 3:
                print("Usage: pattern <pattern>")
                print("Pattern: L=lowercase, U=uppercase, D=digit, S=symbol, X=any, other=literal")
                print("Example: ULLLDDD would generate: Ab12345")
                sys.exit(1)
            
            pattern = sys.argv[2]
            password = generator.generate_custom_pattern(pattern)
            generator.display_password_info(password)
        
        elif command == "config":
            create_password_config()
        
        else:
            print("Unknown command")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
