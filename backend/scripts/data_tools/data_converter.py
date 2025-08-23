from __future__ import annotations
import json
import os
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Any, Dict, List, Optional, Union

class DataConverter:
    def __init__(self):
        self.supported_formats = ['json', 'csv', 'xml', 'txt', 'xlsx']

    # ---------- JSON ----------
    def read_json(self, file_path: str) -> Union[pd.DataFrame, dict, list]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list) and (len(data) == 0 or isinstance(data[0], dict)):
                return pd.DataFrame(data)
            return data
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return None

    def write_json(self, data: Union[pd.DataFrame, dict, list], file_path: str, indent: int = 2) -> bool:
        try:
            if isinstance(data, pd.DataFrame):
                data = data.to_dict(orient='records')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            return True
        except Exception as e:
            print(f"Error writing JSON: {e}")
            return False

    # ---------- CSV ----------
    def read_csv(self, file_path: str, delimiter: str = ',') -> Optional[pd.DataFrame]:
        try:
            return pd.read_csv(file_path, sep=delimiter)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None

    def write_csv(self, data: Union[pd.DataFrame, List[dict]], file_path: str, delimiter: str = ',') -> bool:
        try:
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            data.to_csv(file_path, index=False, sep=delimiter)
            return True
        except Exception as e:
            print(f"Error writing CSV: {e}")
            return False

    # ---------- Excel ----------
    def read_excel(self, file_path: str, sheet_name: Union[str, int] = 0) -> Optional[pd.DataFrame]:
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            print(f"Error reading Excel: {e}")
            return None

    def write_excel(self, data: Union[pd.DataFrame, List[dict]], file_path: str, sheet_name: str = 'Sheet1') -> bool:
        try:
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name=sheet_name, index=False)
            return True
        except Exception as e:
            print(f"Error writing Excel: {e}")
            return False

    # ---------- XML ----------
    def read_xml(self, file_path: str, root_element='root', item_element='item') -> Optional[List[Dict[str, Any]]]:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            rows = []
            for item in root.findall(f'.//{item_element}'):
                row = {child.tag: child.text for child in item}
                for attr_name, attr_value in item.attrib.items():
                    row[f'@{attr_name}'] = attr_value
                rows.append(row)
            return rows
        except Exception as e:
            print(f"Error reading XML: {e}")
            return None

    def write_xml(self, data: Union[pd.DataFrame, List[Dict[str, Any]]], file_path: str, root_element='root', item_element='item') -> bool:
        try:
            if isinstance(data, pd.DataFrame):
                data = data.to_dict(orient='records')
            root = ET.Element(root_element)
            for row in data:
                item = ET.SubElement(root, item_element)
                for k, v in row.items():
                    if k.startswith('@'):
                        item.set(k[1:], str(v))
                    else:
                        child = ET.SubElement(item, str(k))
                        child.text = '' if v is None else str(v)
            xml_str = ET.tostring(root, encoding='utf-8')
            reparsed = minidom.parseString(xml_str)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(reparsed.toprettyxml(indent=" "))
            return True
        except Exception as e:
            print(f"Error writing XML: {e}")
            return False

    # ---------- Flatten / Unflatten ----------
    def flatten_json(self, data: Union[dict, list], separator='.') -> Union[dict, List[dict]]:
        def _flatten(obj, parent_key=''):
            items = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{parent_key}{separator}{k}" if parent_key else k
                    items.extend(_flatten(v, new_key).items())
                return dict(items)
            elif isinstance(obj, list):
                return {parent_key: json.dumps(obj, ensure_ascii=False)}
            else:
                return {parent_key: obj}
        if isinstance(data, list):
            return [_flatten(el) if isinstance(el, (dict, list)) else el for el in data]
        return _flatten(data)

    def unflatten_json(self, data: Union[dict, List[dict]], separator='.') -> Union[dict, List[dict]]:
        def _unflatten(flat_dict):
            result = {}
            for k, v in flat_dict.items():
                parts = k.split(separator)
                d = result
                for part in parts[:-1]:
                    if part not in d:
                        d[part] = {}
                    d = d[part]
                d[parts[-1]] = v
            return result
        if isinstance(data, list):
            return [_unflatten(item) if isinstance(item, dict) else item for item in data]
        return _unflatten(data)

    # ---------- Validation ----------
    def validate_json(self, file_path: str) -> tuple[bool, str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, "Valid JSON"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {e}"
        except Exception as e:
            return False, f"Error reading file: {e}"

    def validate_csv(self, file_path: str, expected_columns: Optional[List[str]] = None) -> tuple[bool, str]:
        try:
            df = self.read_csv(file_path)
            if df is None or df.empty:
                return False, "CSV file is empty or unreadable"
            if expected_columns:
                actual = set(df.columns)
                expected = set(expected_columns)
                missing = expected - actual
                extra = actual - expected
                msg = ""
                if missing:
                    msg += f"Missing columns: {missing}. "
                if extra:
                    msg += f"Extra columns: {extra}. "
                if missing or extra:
                    return False, msg.strip()
            return True, f"Valid CSV with {len(df)} rows"
        except Exception as e:
            return False, f"Error validating CSV: {e}"

    # ---------- Compare ----------
    def compare_data(self, file1: str, file2: str) -> Optional[Dict[str, Any]]:
        data1 = self.auto_read(file1)
        data2 = self.auto_read(file2)
        if data1 is None or data2 is None:
            return None
        if isinstance(data1, pd.DataFrame):
            data1 = data1.to_dict(orient='records')
        if isinstance(data2, pd.DataFrame):
            data2 = data2.to_dict(orient='records')
        if len(data1) != len(data2):
            return {'equal': False, 'reason': f"Different number of records: {len(data1)} vs {len(data2)}"}
        for i, (item1, item2) in enumerate(zip(data1, data2)):
            if item1 != item2:
                return {'equal': False, 'reason': f"Records differ at index {i}", 'record1': item1, 'record2': item2}
        return {'equal': True, 'reason': "Files contain identical data"}

    # ---------- Auto-read ----------
    def auto_read(self, file_path: str) -> Any:
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        try:
            if ext == 'csv':
                return self.read_csv(file_path)
            if ext in ('json',):
                return self.read_json(file_path)
            if ext in ('xls', 'xlsx'):
                return self.read_excel(file_path)
            if ext in ('xml',):
                return self.read_xml(file_path)
            if ext in ('txt',):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            print(f"Unsupported file extension: {ext}")
            return None
        except Exception as e:
            print(f"Error auto-reading {file_path}: {e}")
            return None

    # ---------- Convert ----------
    def convert_file(self, input_path: str, output_path: str) -> bool:
        try:
            data = self.auto_read(input_path)
            if data is None:
                return False
            out_ext = os.path.splitext(output_path)[1].lower().lstrip('.')
            # Tabular outputs
            if out_ext in ('csv', 'xlsx'):
                if isinstance(data, pd.DataFrame):
                    df = data
                elif isinstance(data, list) and (len(data) == 0 or isinstance(data[0], dict)):
                    df = pd.DataFrame(data)
                else:
                    raise ValueError("Input is not tabular; cannot convert to CSV/Excel safely.")
                if out_ext == 'csv':
                    df.to_csv(output_path, index=False)
                else:
                    self.write_excel(df, output_path)
                return True
            if out_ext == 'json':
                return self.write_json(data, output_path)
            if out_ext == 'xml':
                return self.write_xml(data, output_path)
            if out_ext == 'txt':
                payload = data.to_csv(index=False) if isinstance(data, pd.DataFrame) else json.dumps(data, ensure_ascii=False, indent=2) if isinstance(data, (dict, list)) else str(data)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(payload)
                return True
            print(f"Unsupported output extension: {out_ext}")
            return False
        except Exception as e:
            print(f"Error converting file: {e}")
            return False

    # ---------- Sample Files ----------
    def create_sample_files(self, out_dir: str) -> Dict[str, str]:
        os.makedirs(out_dir, exist_ok=True)
        samples = [
            {"id": 1, "name": "A", "score": 88.5},
            {"id": 2, "name": "B", "score": 92.0},
            {"id": 3, "name": "C", "score": 77.0},
        ]
        paths = {}
        df = pd.DataFrame(samples)
        paths['sample.csv'] = os.path.join(out_dir, 'sample.csv'); df.to_csv(paths['sample.csv'], index=False)
        paths['sample.json'] = os.path.join(out_dir, 'sample.json'); self.write_json(df, paths['sample.json'])
        paths['sample.xlsx'] = os.path.join(out_dir, 'sample.xlsx'); self.write_excel(df, paths['sample.xlsx'])
        paths['sample.xml'] = os.path.join(out_dir, 'sample.xml'); self.write_xml(df, paths['sample.xml'])
        paths['sample.txt'] = os.path.join(out_dir, 'sample.txt'); open(paths['sample.txt'], 'w', encoding='utf-8').write("id,name,score\n1,A,88.5\n2,B,92.0\n3,C,77.0\n")
        return paths

    # ---------- NEW FEATURE: Sanitize ----------
    def sanitize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.select_dtypes(include='object'):
            df[col] = df[col].str.strip()
        df.fillna('', inplace=True)
        return df

    # ---------- NEW FEATURE: Preview / Quick Stats ----------
    def preview(self, file_path: str, n: int = 5):
        data = self.auto_read(file_path)
        if isinstance(data, pd.DataFrame):
            print(f"--- Preview of {file_path} ---")
            print(data.head(n))
            print("\nColumns:", list(data.columns))
            print("Data types:\n", data.dtypes)
            print("Missing values:\n", data.isna().sum())
        else:
            print(f"--- Content of {file_path} ---")
            print(str(data)[:500], '...' if len(str(data)) > 500 else '')
