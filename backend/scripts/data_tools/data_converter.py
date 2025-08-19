import json
import csv
import xml.etree.ElementTree as ET
import sys
import os

class DataConverter:
    def __init__(self):
        self.supported_formats = ['json', 'csv', 'xml', 'txt']
    
    def read_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return None
    
    def write_json(self, data, file_path, indent=2):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return False
    
    def read_csv(self, file_path, delimiter=','):
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None
    
    def write_csv(self, data, file_path, delimiter=','):
        try:
            if not data:
                return False
            
            fieldnames = data[0].keys()
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error writing CSV file: {e}")
            return False
    
    def read_xml(self, file_path, root_element='root', item_element='item'):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            data = []
            
            if root.tag == root_element:
                items = root.findall(item_element)
            else:
                items = root.findall(f'.//{item_element}')
            
            for item in items:
                item_data = {}
                for child in item:
                    item_data[child.tag] = child.text
                
                for attr_name, attr_value in item.attrib.items():
                    item_data[f'@{attr_name}'] = attr_value
                
                data.append(item_data)
            
            return data
        except Exception as e:
            print(f"Error reading XML file: {e}")
            return None
    
    def write_xml(self, data, file_path, root_element='root', item_element='item'):
        try:
            root = ET.Element(root_element)
            
            for item in data:
                item_elem = ET.SubElement(root, item_element)
                
                for key, value in item.items():
                    if key.startswith('@'):
                        item_elem.set(key[1:], str(value))
                    else:
                        child_elem = ET.SubElement(item_elem, key)
                        child_elem.text = str(value)
            
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            return True
        except Exception as e:
            print(f"Error writing XML file: {e}")
            return False
    
    def json_to_csv(self, json_file, csv_file):
        data = self.read_json(json_file)
        if data is None:
            return False
        
        if isinstance(data, dict):
            if 'data' in data:
                data = data['data']
            else:
                data = [data]
        
        if not isinstance(data, list):
            print("JSON data must be a list of objects")
            return False
        
        return self.write_csv(data, csv_file)
    
    def csv_to_json(self, csv_file, json_file):
        data = self.read_csv(csv_file)
        if data is None:
            return False
        
        return self.write_json(data, json_file)
    
    def xml_to_json(self, xml_file, json_file):
        data = self.read_xml(xml_file)
        if data is None:
            return False
        
        return self.write_json(data, json_file)
    
    def json_to_xml(self, json_file, xml_file):
        data = self.read_json(json_file)
        if data is None:
            return False
        
        if isinstance(data, dict):
            if 'data' in data:
                data = data['data']
            else:
                data = [data]
        
        return self.write_xml(data, xml_file)
    
    def csv_to_xml(self, csv_file, xml_file):
        data = self.read_csv(csv_file)
        if data is None:
            return False
        
        return self.write_xml(data, xml_file)
    
    def xml_to_csv(self, xml_file, csv_file):
        data = self.read_xml(xml_file)
        if data is None:
            return False
        
        return self.write_csv(data, csv_file)
    
    def flatten_json(self, data, separator='.'):
        def _flatten(obj, parent_key='', separator='.'):
            items = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{parent_key}{separator}{k}" if parent_key else k
                    items.extend(_flatten(v, new_key, separator).items())
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    new_key = f"{parent_key}{separator}{i}" if parent_key else str(i)
                    items.extend(_flatten(v, new_key, separator).items())
            else:
                return {parent_key: obj}
            return dict(items)
        
        if isinstance(data, list):
            return [_flatten(item, '', separator) for item in data]
        else:
            return _flatten(data, '', separator)
    
    def unflatten_json(self, data, separator='.'):
        def _unflatten(flat_dict, separator='.'):
            result = {}
            for key, value in flat_dict.items():
                parts = key.split(separator)
                d = result
                for part in parts[:-1]:
                    if part not in d:
                        d[part] = {}
                    d = d[part]
                d[parts[-1]] = value
            return result
        
        if isinstance(data, list):
            return [_unflatten(item, separator) for item in data]
        else:
            return _unflatten(data, separator)
    
    def validate_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, "Valid JSON"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {e}"
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    def validate_csv(self, file_path, expected_columns=None):
        try:
            data = self.read_csv(file_path)
            if data is None:
                return False, "Could not read CSV file"
            
            if not data:
                return False, "CSV file is empty"
            
            if expected_columns:
                actual_columns = set(data[0].keys())
                expected_set = set(expected_columns)
                
                if actual_columns != expected_set:
                    missing = expected_set - actual_columns
                    extra = actual_columns - expected_set
                    message = ""
                    if missing:
                        message += f"Missing columns: {', '.join(missing)}. "
                    if extra:
                        message += f"Extra columns: {', '.join(extra)}."
                    return False, message
            
            return True, f"Valid CSV with {len(data)} rows"
        except Exception as e:
            return False, f"Error validating CSV: {e}"
    
    def compare_data(self, file1, file2):
        data1 = self.auto_read(file1)
        data2 = self.auto_read(file2)
        
        if data1 is None or data2 is None:
            return None
        
        if len(data1) != len(data2):
            return {
                'equal': False,
                'reason': f"Different number of records: {len(data1)} vs {len(data2)}"
            }
        
        for i, (item1, item2) in enumerate(zip(data1, data2)):
            if item1 != item2:
                return {
                    'equal': False,
                    'reason': f"Records differ at index {i}",
                    'record1': item1,
                    'record2': item2
                }
        
        return {'equal': True, 'reason': 'Files contain identical data'}
    
    def auto_read(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.json':
            return self.read_json(file_path)
        elif ext == '.csv':
            return self.read_csv(file_path)
        elif ext == '.xml':
            return self.read_xml(file_path)
        else:
            print(f"Unsupported file format: {ext}")
            return None
    
    def convert_file(self, input_file, output_file, input_format=None, output_format=None):
        if input_format is None:
            input_format = os.path.splitext(input_file)[1][1:].lower()
        if output_format is None:
            output_format = os.path.splitext(output_file)[1][1:].lower()
        
        conversion_map = {
            ('json', 'csv'): self.json_to_csv,
            ('csv', 'json'): self.csv_to_json,
            ('xml', 'json'): self.xml_to_json,
            ('json', 'xml'): self.json_to_xml,
            ('csv', 'xml'): self.csv_to_xml,
            ('xml', 'csv'): self.xml_to_csv
        }
        
        conversion_func = conversion_map.get((input_format, output_format))
        
        if conversion_func:
            success = conversion_func(input_file, output_file)
            if success:
                print(f"Successfully converted {input_file} to {output_file}")
            return success
        else:
            print(f"Conversion from {input_format} to {output_format} is not supported")
            return False

def create_sample_files():
    converter = DataConverter()
    
    sample_data = [
        {'id': 1, 'name': 'Alice', 'age': 25, 'city': 'New York'},
        {'id': 2, 'name': 'Bob', 'age': 30, 'city': 'London'},
        {'id': 3, 'name': 'Charlie', 'age': 35, 'city': 'Tokyo'}
    ]
    
    converter.write_json(sample_data, 'sample.json')
    converter.write_csv(sample_data, 'sample.csv')
    converter.write_xml(sample_data, 'sample.xml')
    
    print("Sample files created: sample.json, sample.csv, sample.xml")

if __name__ == "__main__":
    converter = DataConverter()
    
    if len(sys.argv) < 2:
        print("Usage: python data_converter.py <command> [args]")
        print("Commands:")
        print("  convert <input> <output>           - Auto-detect and convert")
        print("  json_to_csv <json> <csv>           - Convert JSON to CSV")
        print("  csv_to_json <csv> <json>           - Convert CSV to JSON")
        print("  xml_to_json <xml> <json>           - Convert XML to JSON")
        print("  json_to_xml <json> <xml>           - Convert JSON to XML")
        print("  validate <file>                    - Validate file format")
        print("  compare <file1> <file2>            - Compare two data files")
        print("  flatten <json_file> <output>       - Flatten nested JSON")
        print("  create_sample                      - Create sample files")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "convert":
        if len(sys.argv) < 4:
            print("Usage: convert <input_file> <output_file>")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        converter.convert_file(input_file, output_file)
    
    elif command == "json_to_csv":
        if len(sys.argv) < 4:
            print("Usage: json_to_csv <json_file> <csv_file>")
            sys.exit(1)
        
        converter.json_to_csv(sys.argv[2], sys.argv[3])
    
    elif command == "csv_to_json":
        if len(sys.argv) < 4:
            print("Usage: csv_to_json <csv_file> <json_file>")
            sys.exit(1)
        
        converter.csv_to_json(sys.argv[2], sys.argv[3])
    
    elif command == "xml_to_json":
        if len(sys.argv) < 4:
            print("Usage: xml_to_json <xml_file> <json_file>")
            sys.exit(1)
        
        converter.xml_to_json(sys.argv[2], sys.argv[3])
    
    elif command == "json_to_xml":
        if len(sys.argv) < 4:
            print("Usage: json_to_xml <json_file> <xml_file>")
            sys.exit(1)
        
        converter.json_to_xml(sys.argv[2], sys.argv[3])
    
    elif command == "validate":
        if len(sys.argv) < 3:
            print("Usage: validate <file>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.json':
            valid, message = converter.validate_json(file_path)
        elif ext == '.csv':
            valid, message = converter.validate_csv(file_path)
        else:
            valid, message = False, f"Validation not supported for {ext} files"
        
        print(f"Validation result: {message}")
    
    elif command == "compare":
        if len(sys.argv) < 4:
            print("Usage: compare <file1> <file2>")
            sys.exit(1)
        
        result = converter.compare_data(sys.argv[2], sys.argv[3])
        if result:
            print(f"Comparison result: {result['reason']}")
            if not result['equal'] and 'record1' in result:
                print(f"First differing record: {result['record1']}")
                print(f"Second differing record: {result['record2']}")
    
    elif command == "flatten":
        if len(sys.argv) < 4:
            print("Usage: flatten <json_file> <output_file>")
            sys.exit(1)
        
        data = converter.read_json(sys.argv[2])
        if data:
            flattened = converter.flatten_json(data)
            converter.write_json(flattened, sys.argv[3])
            print(f"Flattened JSON saved to {sys.argv[3]}")
    
    elif command == "create_sample":
        create_sample_files()
    
    else:
        print("Unknown command")
