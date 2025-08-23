import datetime
import sys


class AgeCalculator:
    def __init__(self):
        self.months_in_year = 12
        self.days_in_year = 365.25
        self.hours_in_day = 24
        self.minutes_in_hour = 60
        self.seconds_in_minute = 60
    
    def parse_date(self, date_string):
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%d.%m.%Y",
            "%B %d, %Y",
            "%d %B %Y"
        ]
        
        for format_str in formats:
            try:
                return datetime.datetime.strptime(date_string, format_str).date()
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_string}")
    
    def calculate_age(self, birth_date, current_date=None):
        if isinstance(birth_date, str):
            birth_date = self.parse_date(birth_date)
        
        if current_date is None:
            current_date = datetime.date.today()
        elif isinstance(current_date, str):
            current_date = self.parse_date(current_date)
        
        if birth_date > current_date:
            raise ValueError("Birth date cannot be in the future")
        
        age_years = current_date.year - birth_date.year
        
        if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
            age_years -= 1
        
        next_birthday = datetime.date(current_date.year, birth_date.month, birth_date.day)
        if next_birthday < current_date:
            next_birthday = datetime.date(current_date.year + 1, birth_date.month, birth_date.day)
        
        days_to_birthday = (next_birthday - current_date).days
        
        total_days = (current_date - birth_date).days
        total_weeks = total_days // 7
        total_months = age_years * 12 + (current_date.month - birth_date.month)
        
        if current_date.day < birth_date.day:
            total_months -= 1
        
        total_hours = total_days * 24
        total_minutes = total_hours * 60
        total_seconds = total_minutes * 60
        
        return {
            'years': age_years,
            'months': total_months,
            'weeks': total_weeks,
            'days': total_days,
            'hours': total_hours,
            'minutes': total_minutes,
            'seconds': total_seconds,
            'days_to_next_birthday': days_to_birthday,
            'next_birthday': next_birthday,
            'birth_date': birth_date,
            'calculation_date': current_date
        }
    
    def get_detailed_age(self, birth_date, current_date=None):
        if isinstance(birth_date, str):
            birth_date = self.parse_date(birth_date)
        
        if current_date is None:
            current_date = datetime.date.today()
        elif isinstance(current_date, str):
            current_date = self.parse_date(current_date)
        
        years = current_date.year - birth_date.year
        months = current_date.month - birth_date.month
        days = current_date.day - birth_date.day
        
        if days < 0:
            months -= 1
            last_month = current_date.replace(day=1) - datetime.timedelta(days=1)
            days += last_month.day
        
        if months < 0:
            years -= 1
            months += 12
        
        return {
            'years': years,
            'months': months,
            'days': days
        }
    
    def calculate_zodiac_sign(self, birth_date):
        if isinstance(birth_date, str):
            birth_date = self.parse_date(birth_date)
        
        month = birth_date.month
        day = birth_date.day
        
        zodiac_signs = [
            ((1, 20), (2, 18), "Aquarius", "♒"),
            ((2, 19), (3, 20), "Pisces", "♓"),
            ((3, 21), (4, 19), "Aries", "♈"),
            ((4, 20), (5, 20), "Taurus", "♉"),
            ((5, 21), (6, 20), "Gemini", "♊"),
            ((6, 21), (7, 22), "Cancer", "♋"),
            ((7, 23), (8, 22), "Leo", "♌"),
            ((8, 23), (9, 22), "Virgo", "♍"),
            ((9, 23), (10, 22), "Libra", "♎"),
            ((10, 23), (11, 21), "Scorpio", "♏"),
            ((11, 22), (12, 21), "Sagittarius", "♐"),
            ((12, 22), (1, 19), "Capricorn", "♑")
        ]
        
        for start, end, sign, symbol in zodiac_signs:
            if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
                return {"sign": sign, "symbol": symbol}
        
        return {"sign": "Unknown", "symbol": "?"}
    
    def calculate_chinese_zodiac(self, birth_date):
        if isinstance(birth_date, str):
            birth_date = self.parse_date(birth_date)
        
        animals = [
            "Monkey", "Rooster", "Dog", "Pig", "Rat", "Ox",
            "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat"
        ]
        
        year = birth_date.year
        animal_index = year % 12
        
        elements = ["Metal", "Water", "Wood", "Fire", "Earth"]
        element_index = (year // 2) % 5
        
        return {
            "animal": animals[animal_index],
            "element": elements[element_index],
            "year": year
        }
    
    def calculate_life_events(self, birth_date):
        if isinstance(birth_date, str):
            birth_date = self.parse_date(birth_date)
        
        today = datetime.date.today()
        
        milestones = [
            (18, "Legal adult"),
            (21, "Legal drinking age (US)"),
            (25, "Quarter century"),
            (30, "Thirty"),
            (40, "Forty"),
            (50, "Half century"),
            (65, "Retirement age"),
            (100, "Centennial")
        ]
        
        events = []
        
        for age, description in milestones:
            milestone_date = datetime.date(birth_date.year + age, birth_date.month, birth_date.day)
            
            if milestone_date <= today:
                days_ago = (today - milestone_date).days
                events.append({
                    "age": age,
                    "description": description,
                    "date": milestone_date,
                    "status": "passed",
                    "days_ago": days_ago
                })
            else:
                days_until = (milestone_date - today).days
                events.append({
                    "age": age,
                    "description": description,
                    "date": milestone_date,
                    "status": "upcoming",
                    "days_until": days_until
                })
        
        return events
    
    def display_age_info(self, birth_date, current_date=None):
        age_data = self.calculate_age(birth_date, current_date)
        detailed_age = self.get_detailed_age(birth_date, current_date)
        zodiac = self.calculate_zodiac_sign(birth_date)
        chinese_zodiac = self.calculate_chinese_zodiac(birth_date)
        
        print("\n🎂 AGE CALCULATOR RESULTS")
        print("="*50)
        print(f"Birth Date: {age_data['birth_date'].strftime('%B %d, %Y')}")
        print(f"Current Date: {age_data['calculation_date'].strftime('%B %d, %Y')}")
        print()
        
        print("📅 Exact Age:")
        print(f"   {detailed_age['years']} years, {detailed_age['months']} months, {detailed_age['days']} days")
        print()
        
        print("📊 Age Breakdown:")
        print(f"   Years: {age_data['years']:,}")
        print(f"   Months: {age_data['months']:,}")
        print(f"   Weeks: {age_data['weeks']:,}")
        print(f"   Days: {age_data['days']:,}")
        print(f"   Hours: {age_data['hours']:,}")
        print(f"   Minutes: {age_data['minutes']:,}")
        print(f"   Seconds: {age_data['seconds']:,}")
        print()
        
        print("🎉 Next Birthday:")
        print(f"   Date: {age_data['next_birthday'].strftime('%B %d, %Y')}")
        print(f"   Days until: {age_data['days_to_birthday']}")
        print(f"   You'll turn: {age_data['years'] + 1}")
        print()
        
        print("⭐ Zodiac Information:")
        print(f"   Western: {zodiac['sign']} {zodiac['symbol']}")
        print(f"   Chinese: {chinese_zodiac['element']} {chinese_zodiac['animal']} ({chinese_zodiac['year']})")
        print()
        
        print("="*50)
    
    def display_life_events(self, birth_date):
        events = self.calculate_life_events(birth_date)
        
        print("\n🌟 LIFE MILESTONES")
        print("="*50)
        
        passed_events = [e for e in events if e['status'] == 'passed']
        upcoming_events = [e for e in events if e['status'] == 'upcoming']
        
        if passed_events:
            print("✅ Milestones Reached:")
            for event in passed_events[:5]:
                print(f"   {event['description']} (Age {event['age']}) - {event['days_ago']} days ago")
            print()
        
        if upcoming_events:
            print("🔮 Upcoming Milestones:")
            for event in upcoming_events[:5]:
                print(f"   {event['description']} (Age {event['age']}) - in {event['days_until']} days")
                print(f"      Date: {event['date'].strftime('%B %d, %Y')}")
        
        print("="*50)
    
    def compare_ages(self, person1_birth, person2_birth, person1_name="Person 1", person2_name="Person 2"):
        if isinstance(person1_birth, str):
            person1_birth = self.parse_date(person1_birth)
        if isinstance(person2_birth, str):
            person2_birth = self.parse_date(person2_birth)
        
        age1 = self.calculate_age(person1_birth)
        age2 = self.calculate_age(person2_birth)
        
        age_difference = abs((person1_birth - person2_birth).days)
        older_person = person1_name if person1_birth < person2_birth else person2_name
        
        print(f"\n👥 AGE COMPARISON")
        print("="*40)
        print(f"{person1_name}: {age1['years']} years old")
        print(f"{person2_name}: {age2['years']} years old")
        print(f"Age difference: {age_difference} days ({age_difference/365.25:.1f} years)")
        print(f"Older person: {older_person}")
        print("="*40)

if __name__ == "__main__":
    calculator = AgeCalculator()
    
    if len(sys.argv) < 2:
        print("Usage: python age_calculator.py <command> [args]")
        print("Commands:")
        print("  age <birth_date> [current_date]     - Calculate age")
        print("  milestones <birth_date>             - Show life milestones")
        print("  compare <birth1> <birth2> [name1] [name2] - Compare two ages")
        print("  zodiac <birth_date>                 - Show zodiac signs")
        print("\nDate formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, DD-MM-YYYY")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "age":
            if len(sys.argv) < 3:
                print("Usage: age <birth_date> [current_date]")
                sys.exit(1)
            
            birth_date = sys.argv[2]
            current_date = sys.argv[3] if len(sys.argv) > 3 else None
            
            calculator.display_age_info(birth_date, current_date)
        
        elif command == "milestones":
            if len(sys.argv) < 3:
                print("Usage: milestones <birth_date>")
                sys.exit(1)
            
            birth_date = sys.argv[2]
            calculator.display_life_events(birth_date)
        
        elif command == "compare":
            if len(sys.argv) < 4:
                print("Usage: compare <birth_date1> <birth_date2> [name1] [name2]")
                sys.exit(1)
            
            birth1 = sys.argv[2]
            birth2 = sys.argv[3]
            name1 = sys.argv[4] if len(sys.argv) > 4 else "Person 1"
            name2 = sys.argv[5] if len(sys.argv) > 5 else "Person 2"
            
            calculator.compare_ages(birth1, birth2, name1, name2)
        
        elif command == "zodiac":
            if len(sys.argv) < 3:
                print("Usage: zodiac <birth_date>")
                sys.exit(1)
            
            birth_date = sys.argv[2]
            zodiac = calculator.calculate_zodiac_sign(birth_date)
            chinese = calculator.calculate_chinese_zodiac(birth_date)
            
            print(f"\n⭐ ZODIAC INFORMATION")
            print("="*30)
            print(f"Western Zodiac: {zodiac['sign']} {zodiac['symbol']}")
            print(f"Chinese Zodiac: {chinese['element']} {chinese['animal']}")
            print("="*30)
        
        else:
            print("Unknown command")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
