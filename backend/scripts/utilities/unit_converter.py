import sys
import math

class UnitConverter:
    def __init__(self):
        self.conversions = {
            'length': {
                'mm': 0.001,
                'cm': 0.01,
                'm': 1.0,
                'km': 1000.0,
                'in': 0.0254,
                'ft': 0.3048,
                'yd': 0.9144,
                'mile': 1609.34,
                'nmi': 1852.0
            },
            'weight': {
                'mg': 0.000001,
                'g': 0.001,
                'kg': 1.0,
                'oz': 0.0283495,
                'lb': 0.453592,
                'stone': 6.35029,
                'ton': 1000.0
            },
            'temperature': {
                'celsius': 'celsius',
                'fahrenheit': 'fahrenheit',
                'kelvin': 'kelvin',
                'rankine': 'rankine'
            },
            'area': {
                'mm2': 0.000001,
                'cm2': 0.0001,
                'm2': 1.0,
                'km2': 1000000.0,
                'in2': 0.00064516,
                'ft2': 0.092903,
                'yd2': 0.836127,
                'acre': 4046.86,
                'hectare': 10000.0
            },
            'volume': {
                'ml': 0.000001,
                'l': 0.001,
                'm3': 1.0,
                'in3': 0.0000163871,
                'ft3': 0.0283168,
                'gal_us': 0.00378541,
                'gal_uk': 0.00454609,
                'qt': 0.000946353,
                'pt': 0.000473176,
                'cup': 0.000236588,
                'fl_oz': 0.0000295735
            },
            'speed': {
                'mps': 1.0,
                'kph': 0.277778,
                'mph': 0.44704,
                'fps': 0.3048,
                'knot': 0.514444
            },
            'pressure': {
                'pa': 1.0,
                'kpa': 1000.0,
                'bar': 100000.0,
                'atm': 101325.0,
                'psi': 6894.76,
                'mmhg': 133.322,
                'torr': 133.322
            },
            'energy': {
                'j': 1.0,
                'kj': 1000.0,
                'cal': 4.184,
                'kcal': 4184.0,
                'btu': 1055.06,
                'kwh': 3600000.0,
                'wh': 3600.0
            },
            'data': {
                'b': 1.0,
                'kb': 1024.0,
                'mb': 1048576.0,
                'gb': 1073741824.0,
                'tb': 1099511627776.0,
                'pb': 1125899906842624.0
            }
        }
        
        self.unit_names = {
            'length': {
                'mm': 'Millimeter', 'cm': 'Centimeter', 'm': 'Meter', 'km': 'Kilometer',
                'in': 'Inch', 'ft': 'Foot', 'yd': 'Yard', 'mile': 'Mile', 'nmi': 'Nautical Mile'
            },
            'weight': {
                'mg': 'Milligram', 'g': 'Gram', 'kg': 'Kilogram', 'oz': 'Ounce',
                'lb': 'Pound', 'stone': 'Stone', 'ton': 'Metric Ton'
            },
            'temperature': {
                'celsius': 'Celsius', 'fahrenheit': 'Fahrenheit', 'kelvin': 'Kelvin', 'rankine': 'Rankine'
            },
            'area': {
                'mm2': 'Square Millimeter', 'cm2': 'Square Centimeter', 'm2': 'Square Meter',
                'km2': 'Square Kilometer', 'in2': 'Square Inch', 'ft2': 'Square Foot',
                'yd2': 'Square Yard', 'acre': 'Acre', 'hectare': 'Hectare'
            },
            'volume': {
                'ml': 'Milliliter', 'l': 'Liter', 'm3': 'Cubic Meter', 'in3': 'Cubic Inch',
                'ft3': 'Cubic Foot', 'gal_us': 'US Gallon', 'gal_uk': 'UK Gallon',
                'qt': 'Quart', 'pt': 'Pint', 'cup': 'Cup', 'fl_oz': 'Fluid Ounce'
            },
            'speed': {
                'mps': 'Meters per Second', 'kph': 'Kilometers per Hour', 'mph': 'Miles per Hour',
                'fps': 'Feet per Second', 'knot': 'Knot'
            },
            'pressure': {
                'pa': 'Pascal', 'kpa': 'Kilopascal', 'bar': 'Bar', 'atm': 'Atmosphere',
                'psi': 'Pounds per Square Inch', 'mmhg': 'Millimeters of Mercury', 'torr': 'Torr'
            },
            'energy': {
                'j': 'Joule', 'kj': 'Kilojoule', 'cal': 'Calorie', 'kcal': 'Kilocalorie',
                'btu': 'British Thermal Unit', 'kwh': 'Kilowatt Hour', 'wh': 'Watt Hour'
            },
            'data': {
                'b': 'Byte', 'kb': 'Kilobyte', 'mb': 'Megabyte', 'gb': 'Gigabyte',
                'tb': 'Terabyte', 'pb': 'Petabyte'
            }
        }
    
    def convert_temperature(self, value, from_unit, to_unit):
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit == to_unit:
            return value
        
        celsius_value = value
        
        if from_unit == 'fahrenheit':
            celsius_value = (value - 32) * 5/9
        elif from_unit == 'kelvin':
            celsius_value = value - 273.15
        elif from_unit == 'rankine':
            celsius_value = (value - 491.67) * 5/9
        
        if to_unit == 'celsius':
            return celsius_value
        elif to_unit == 'fahrenheit':
            return celsius_value * 9/5 + 32
        elif to_unit == 'kelvin':
            return celsius_value + 273.15
        elif to_unit == 'rankine':
            return (celsius_value + 273.15) * 9/5
        
        return None
    
    def convert_standard(self, value, from_unit, to_unit, category):
        if category not in self.conversions:
            return None
        
        units = self.conversions[category]
        
        if from_unit not in units or to_unit not in units:
            return None
        
        if from_unit == to_unit:
            return value
        
        base_value = value * units[from_unit]
        result = base_value / units[to_unit]
        
        return result
    
    def convert(self, value, from_unit, to_unit, category=None):
        if category is None:
            category = self.detect_category(from_unit, to_unit)
            if category is None:
                return None
        
        if category == 'temperature':
            return self.convert_temperature(value, from_unit, to_unit)
        else:
            return self.convert_standard(value, from_unit, to_unit, category)
    
    def detect_category(self, from_unit, to_unit):
        for category, units in self.conversions.items():
            if from_unit in units and to_unit in units:
                return category
        return None
    
    def list_categories(self):
        return list(self.conversions.keys())
    
    def list_units(self, category):
        if category in self.conversions:
            return list(self.conversions[category].keys())
        return []
    
    def get_unit_name(self, unit, category):
        if category in self.unit_names and unit in self.unit_names[category]:
            return self.unit_names[category][unit]
        return unit.upper()
    
    def format_result(self, value, from_value, from_unit, to_unit, category):
        from_name = self.get_unit_name(from_unit, category)
        to_name = self.get_unit_name(to_unit, category)
        
        if value is None:
            print(f"Cannot convert {from_unit} to {to_unit}")
            return
        
        precision = 6 if abs(value) < 1 else 4 if abs(value) < 100 else 2
        
        print(f"\n🔄 UNIT CONVERSION")
        print("="*40)
        print(f"Category: {category.title()}")
        print(f"From: {from_value:g} {from_name} ({from_unit})")
        print(f"To:   {value:.{precision}g} {to_name} ({to_unit})")
        print("="*40)
        
        return value
    
    def convert_multiple(self, value, from_unit, category, target_units=None):
        if category not in self.conversions:
            print(f"Unknown category: {category}")
            return
        
        if target_units is None:
            target_units = list(self.conversions[category].keys())
        
        print(f"\n📐 MULTIPLE CONVERSIONS")
        print(f"Base: {value:g} {self.get_unit_name(from_unit, category)}")
        print("="*50)
        
        for unit in target_units:
            if unit != from_unit:
                result = self.convert(value, from_unit, unit, category)
                if result is not None:
                    unit_name = self.get_unit_name(unit, category)
                    precision = 6 if abs(result) < 1 else 4 if abs(result) < 100 else 2
                    print(f"{unit}: {result:.{precision}g} {unit_name}")
        
        print("="*50)
    
    def calculate_ratio(self, value1, unit1, value2, unit2, category):
        if category not in self.conversions:
            return None
        
        base1 = value1 * self.conversions[category].get(unit1, 0)
        base2 = value2 * self.conversions[category].get(unit2, 0)
        
        if base2 == 0:
            return None
        
        return base1 / base2
    
    def find_best_unit(self, value, from_unit, category):
        if category not in self.conversions:
            return from_unit
        
        base_value = value * self.conversions[category].get(from_unit, 1)
        
        best_unit = from_unit
        best_value = abs(value)
        
        for unit, factor in self.conversions[category].items():
            converted = base_value / factor
            if 1 <= abs(converted) < best_value or (best_value < 1 and abs(converted) >= 1):
                best_unit = unit
                best_value = abs(converted)
        
        return best_unit
    
    def smart_convert(self, value, from_unit):
        category = None
        for cat, units in self.conversions.items():
            if from_unit in units:
                category = cat
                break
        
        if category is None:
            print(f"Unknown unit: {from_unit}")
            return
        
        best_unit = self.find_best_unit(value, from_unit, category)
        result = self.convert(value, from_unit, best_unit, category)
        
        self.format_result(result, value, from_unit, best_unit, category)

if __name__ == "__main__":
    converter = UnitConverter()
    
    if len(sys.argv) < 2:
        print("Usage: python unit_converter.py <command> [args]")
        print("Commands:")
        print("  convert <value> <from_unit> <to_unit> [category]")
        print("  multiple <value> <from_unit> <category> [target_units]")
        print("  smart <value> <unit>")
        print("  categories")
        print("  units <category>")
        print("  ratio <val1> <unit1> <val2> <unit2> <category>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "convert":
        if len(sys.argv) < 5:
            print("Usage: convert <value> <from_unit> <to_unit> [category]")
            sys.exit(1)
        
        try:
            value = float(sys.argv[2])
            from_unit = sys.argv[3].lower()
            to_unit = sys.argv[4].lower()
            category = sys.argv[5] if len(sys.argv) > 5 else None
            
            result = converter.convert(value, from_unit, to_unit, category)
            
            if category is None:
                category = converter.detect_category(from_unit, to_unit)
            
            converter.format_result(result, value, from_unit, to_unit, category)
        
        except ValueError:
            print("Invalid value. Please enter a number.")
    
    elif command == "multiple":
        if len(sys.argv) < 5:
            print("Usage: multiple <value> <from_unit> <category> [target_units]")
            sys.exit(1)
        
        try:
            value = float(sys.argv[2])
            from_unit = sys.argv[3].lower()
            category = sys.argv[4].lower()
            target_units = sys.argv[5].split(',') if len(sys.argv) > 5 else None
            
            converter.convert_multiple(value, from_unit, category, target_units)
        
        except ValueError:
            print("Invalid value. Please enter a number.")
    
    elif command == "smart":
        if len(sys.argv) < 4:
            print("Usage: smart <value> <unit>")
            sys.exit(1)
        
        try:
            value = float(sys.argv[2])
            unit = sys.argv[3].lower()
            
            converter.smart_convert(value, unit)
        
        except ValueError:
            print("Invalid value. Please enter a number.")
    
    elif command == "categories":
        categories = converter.list_categories()
        print("\nAvailable Categories:")
        print("="*30)
        for category in categories:
            print(f"- {category.title()}")
    
    elif command == "units":
        if len(sys.argv) < 3:
            print("Usage: units <category>")
            sys.exit(1)
        
        category = sys.argv[2].lower()
        units = converter.list_units(category)
        
        if units:
            print(f"\nUnits in {category.title()}:")
            print("="*30)
            for unit in units:
                name = converter.get_unit_name(unit, category)
                print(f"{unit}: {name}")
        else:
            print(f"Unknown category: {category}")
    
    elif command == "ratio":
        if len(sys.argv) < 7:
            print("Usage: ratio <val1> <unit1> <val2> <unit2> <category>")
            sys.exit(1)
        
        try:
            val1 = float(sys.argv[2])
            unit1 = sys.argv[3].lower()
            val2 = float(sys.argv[4])
            unit2 = sys.argv[5].lower()
            category = sys.argv[6].lower()
            
            ratio = converter.calculate_ratio(val1, unit1, val2, unit2, category)
            
            if ratio is not None:
                print(f"\nRatio: {val1} {unit1} : {val2} {unit2} = {ratio:.4f} : 1")
            else:
                print("Cannot calculate ratio")
        
        except ValueError:
            print("Invalid values. Please enter numbers.")
    
    else:
        print("Unknown command")
