import hashlib
import hmac
import secrets
import string
import re
import sys

class PasswordChecker:
    def __init__(self):
        self.common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123', 'password123',
            'admin', 'letmein', 'welcome', 'monkey', '1234567890', 'password1',
            'qwerty123', 'dragon', 'master', 'hello', 'login', 'welcome123'
        ]
        
        self.password_patterns = [
            '123', '321', 'abc', 'qwe', 'asd', 'zxc', '111', '000',
            'password', 'admin', 'root', 'user', 'guest', 'test'
        ]
    
    def calculate_entropy(self, password):
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)
        
        if charset_size == 0:
            return 0
        
        import math
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    def check_common_patterns(self, password):
        password_lower = password.lower()
        found_patterns = []
        
        for pattern in self.password_patterns:
            if pattern in password_lower:
                found_patterns.append(pattern)
        
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '12345', '54321']
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                found_patterns.append(f"keyboard pattern: {pattern}")
        
        return found_patterns
    
    def check_character_variety(self, password):
        checks = {
            'lowercase': any(c.islower() for c in password),
            'uppercase': any(c.isupper() for c in password),
            'digits': any(c.isdigit() for c in password),
            'special': any(c in string.punctuation for c in password),
            'length_8_plus': len(password) >= 8,
            'length_12_plus': len(password) >= 12
        }
        
        return checks
    
    def check_repeated_characters(self, password):
        repeated_chars = []
        repeated_sequences = []
        
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                repeated_chars.append(password[i:i+3])
        
        for i in range(len(password) - 3):
            sequence = password[i:i+4]
            if len(set(sequence)) <= 2:
                repeated_sequences.append(sequence)
        
        return {
            'repeated_chars': list(set(repeated_chars)),
            'repeated_sequences': list(set(repeated_sequences))
        }
    
    def check_dictionary_words(self, password):
        common_words = [
            'password', 'admin', 'user', 'root', 'guest', 'test', 'demo',
            'login', 'access', 'secret', 'private', 'secure', 'system'
        ]
        
        password_lower = password.lower()
        found_words = []
        
        for word in common_words:
            if word in password_lower:
                found_words.append(word)
        
        return found_words
    
    def estimate_crack_time(self, password):
        entropy = self.calculate_entropy(password)
        
        attempts_per_second = {
            'online_throttled': 1000,
            'online_unthrottled': 1000000,
            'offline_slow': 100000000,
            'offline_fast': 10000000000
        }
        
        crack_times = {}
        
        for scenario, rate in attempts_per_second.items():
            time_seconds = (2 ** entropy) / (2 * rate)
            
            if time_seconds < 60:
                time_str = f"{time_seconds:.1f} seconds"
            elif time_seconds < 3600:
                time_str = f"{time_seconds/60:.1f} minutes"
            elif time_seconds < 86400:
                time_str = f"{time_seconds/3600:.1f} hours"
            elif time_seconds < 31536000:
                time_str = f"{time_seconds/86400:.1f} days"
            else:
                time_str = f"{time_seconds/31536000:.1f} years"
            
            crack_times[scenario] = time_str
        
        return crack_times
    
    def analyze_password(self, password):
        if not password:
            return {'error': 'Password cannot be empty'}
        
        analysis = {
            'password': password,
            'length': len(password),
            'entropy': self.calculate_entropy(password),
            'character_variety': self.check_character_variety(password),
            'common_patterns': self.check_common_patterns(password),
            'repeated_elements': self.check_repeated_characters(password),
            'dictionary_words': self.check_dictionary_words(password),
            'is_common': password.lower() in self.common_passwords,
            'crack_times': self.estimate_crack_time(password)
        }
        
        strength_score = self.calculate_strength_score(analysis)
        analysis['strength_score'] = strength_score
        analysis['strength_level'] = self.get_strength_level(strength_score)
        
        return analysis
    
    def calculate_strength_score(self, analysis):
        score = 0
        
        if analysis['length'] >= 8:
            score += 1
        if analysis['length'] >= 12:
            score += 1
        if analysis['length'] >= 16:
            score += 1
        
        char_variety = analysis['character_variety']
        score += sum([
            char_variety['lowercase'],
            char_variety['uppercase'],
            char_variety['digits'],
            char_variety['special']
        ])
        
        if analysis['entropy'] > 50:
            score += 1
        if analysis['entropy'] > 70:
            score += 1
        
        if not analysis['common_patterns']:
            score += 1
        
        if not analysis['repeated_elements']['repeated_chars']:
            score += 1
        
        if not analysis['dictionary_words']:
            score += 1
        
        if not analysis['is_common']:
            score += 1
        
        return min(score, 12)
    
    def get_strength_level(self, score):
        if score <= 3:
            return "Very Weak"
        elif score <= 5:
            return "Weak"
        elif score <= 7:
            return "Fair"
        elif score <= 9:
            return "Good"
        elif score <= 11:
            return "Strong"
        else:
            return "Very Strong"
    
    def get_recommendations(self, analysis):
        recommendations = []
        
        if analysis['length'] < 8:
            recommendations.append("Use at least 8 characters")
        elif analysis['length'] < 12:
            recommendations.append("Consider using 12+ characters for better security")
        
        char_variety = analysis['character_variety']
        if not char_variety['lowercase']:
            recommendations.append("Add lowercase letters")
        if not char_variety['uppercase']:
            recommendations.append("Add uppercase letters")
        if not char_variety['digits']:
            recommendations.append("Add numbers")
        if not char_variety['special']:
            recommendations.append("Add special characters (!@#$%^&*)")
        
        if analysis['common_patterns']:
            recommendations.append(f"Avoid common patterns: {', '.join(analysis['common_patterns'])}")
        
        if analysis['repeated_elements']['repeated_chars']:
            recommendations.append("Avoid repeating the same character multiple times")
        
        if analysis['dictionary_words']:
            recommendations.append(f"Avoid dictionary words: {', '.join(analysis['dictionary_words'])}")
        
        if analysis['is_common']:
            recommendations.append("This is a commonly used password - choose something unique")
        
        if analysis['entropy'] < 50:
            recommendations.append("Increase password complexity for better entropy")
        
        return recommendations
    
    def display_analysis(self, analysis):
        if 'error' in analysis:
            print(f"Error: {analysis['error']}")
            return
        
        print(f"\n🔐 PASSWORD STRENGTH ANALYSIS")
        print("="*50)
        print(f"Password: {'*' * len(analysis['password'])}")
        print(f"Length: {analysis['length']} characters")
        print(f"Strength: {analysis['strength_level']} ({analysis['strength_score']}/12)")
        print(f"Entropy: {analysis['entropy']:.1f} bits")
        
        print(f"\n📊 Character Variety:")
        variety = analysis['character_variety']
        print(f"  Lowercase: {'✓' if variety['lowercase'] else '✗'}")
        print(f"  Uppercase: {'✓' if variety['uppercase'] else '✗'}")
        print(f"  Digits: {'✓' if variety['digits'] else '✗'}")
        print(f"  Special chars: {'✓' if variety['special'] else '✗'}")
        
        if analysis['common_patterns']:
            print(f"\n⚠️  Common patterns found: {', '.join(analysis['common_patterns'])}")
        
        if analysis['repeated_elements']['repeated_chars']:
            print(f"\n⚠️  Repeated characters: {', '.join(analysis['repeated_elements']['repeated_chars'])}")
        
        if analysis['dictionary_words']:
            print(f"\n⚠️  Dictionary words: {', '.join(analysis['dictionary_words'])}")
        
        if analysis['is_common']:
            print(f"\n⚠️  This is a commonly used password!")
        
        print(f"\n⏱️  Estimated crack times:")
        for scenario, time in analysis['crack_times'].items():
            scenario_name = scenario.replace('_', ' ').title()
            print(f"  {scenario_name}: {time}")
        
        recommendations = self.get_recommendations(analysis)
        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"  • {rec}")
        
        print("="*50)

if __name__ == "__main__":
    checker = PasswordChecker()
    
    if len(sys.argv) < 2:
        print("Usage: python password_checker.py <command> [args]")
        print("Commands:")
        print("  check <password>     - Analyze password strength")
        print("  test                 - Test with sample passwords")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 3:
            password = input("Enter password to analyze: ")
        else:
            password = sys.argv[2]
        
        analysis = checker.analyze_password(password)
        checker.display_analysis(analysis)
    
    elif command == "test":
        test_passwords = [
            "123456",
            "password",
            "Password123",
            "MyS3cur3P@ssw0rd!",
            "qwerty123",
            "Tr0ub4dor&3"
        ]
        
        for pwd in test_passwords:
            print(f"\nTesting: {pwd}")
            analysis = checker.analyze_password(pwd)
            print(f"Strength: {analysis['strength_level']} ({analysis['strength_score']}/12)")
    
    else:
        print("Unknown command")
