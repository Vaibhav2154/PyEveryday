from __future__ import annotations
import os
import sys
from typing import Any, Dict, List, Optional, Union
import pandas as pd


class DataProcessor:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    # ----------------- IO -----------------
    def read_data(self, file_path: str, chunk_size: Optional[int] = None) -> Union[pd.DataFrame, pd.io.parsers.TextFileReader]:
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if ext == 'csv':
            return pd.read_csv(file_path, chunksize=chunk_size) if chunk_size else pd.read_csv(file_path)
        if ext in ('json',):
            if chunk_size:
                return pd.read_json(file_path, lines=True, chunksize=chunk_size)
            data = pd.read_json(file_path)
            if isinstance(data, dict):
                return pd.json_normalize(data)
            return data
        if ext in ('xls', 'xlsx'):
            return pd.read_excel(file_path)
        if ext == 'txt':
            return pd.read_csv(file_path, delimiter='\t')
        raise ValueError(f"Unsupported format: {ext}")

    def write_data(self, data: Union[pd.DataFrame, pd.io.parsers.TextFileReader], file_path: str, format_type: Optional[str] = None) -> None:
        ext = (format_type or os.path.splitext(file_path)[1].lower().lstrip('.'))
        if ext == 'csv':
            if hasattr(data, '__iter__') and not isinstance(data, pd.DataFrame):
                first = True
                for chunk in data:
                    chunk.to_csv(file_path, index=False, mode='w' if first else 'a', header=first)
                    first = False
            else:
                data.to_csv(file_path, index=False)
        elif ext == 'json':
            if hasattr(data, '__iter__') and not isinstance(data, pd.DataFrame):
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chunk in data:
                        for rec in chunk.to_dict(orient='records'):
                            f.write(pd.io.json.dumps(rec, force_ascii=False) + '\n')
            else:
                data.to_json(file_path, orient='records', force_ascii=False, indent=2)
        elif ext in ('xls', 'xlsx'):
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                data.to_excel(writer, index=False)
        else:
            raise ValueError(f"Unsupported format: {ext}")
        if self.verbose:
            print(f"Data saved to {file_path}")

    # ----------------- Info -----------------
    def get_data_info(self, data: pd.DataFrame) -> Dict[str, Any]:
        return {
            "rows": int(data.shape[0]),
            "columns": int(data.shape[1]),
            "dtypes": {c: str(t) for c, t in data.dtypes.to_dict().items()},
            "null_counts": data.isna().sum().to_dict(),
            "duplicates": int(data.duplicated().sum()),
            "memory_usage": int(data.memory_usage(deep=True).sum())
        }

    def preview_data(self, data: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        return data.head(n)

    def get_shape(self, data: pd.DataFrame) -> tuple:
        return data.shape

    # ----------------- Cleaning -----------------
    def clean_data(self, data: pd.DataFrame, operations: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        df = data.copy()
        if operations is None:
            operations = {"drop_duplicates": True, "fill_nulls": True, "strip_strings": True}

        if operations.get("drop_duplicates"):
            before = len(df)
            df = df.drop_duplicates()
            if self.verbose:
                print(f"Removed {before - len(df)} duplicate rows")

        if operations.get("fill_nulls"):
            for col in df.columns:
                if df[col].dtype == 'object':
                    nulls = df[col].isna().sum()
                    df[col] = df[col].fillna("Unknown")
                    if self.verbose and nulls > 0:
                        print(f"Filled {nulls} nulls in column '{col}' with 'Unknown'")
                else:
                    nulls = df[col].isna().sum()
                    df[col] = df[col].fillna(df[col].mean())
                    if self.verbose and nulls > 0:
                        print(f"Filled {nulls} nulls in column '{col}' with mean value")

        if operations.get("strip_strings"):
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
                if self.verbose:
                    print(f"Stripped whitespace in column '{col}'")

        return df

    # ----------------- Filtering -----------------
    def filter_data(self, data: pd.DataFrame, conditions: List[Dict[str, Any]]) -> pd.DataFrame:
        df = data.copy()
        for cond in conditions:
            col = cond["column"]
            op = cond["operator"]
            val = cond.get("value")
            if op == "equals":
                df = df[df[col] == val]
            elif op == "not_equals":
                df = df[df[col] != val]
            elif op == "greater_than":
                df = df[df[col] > val]
            elif op == "less_than":
                df = df[df[col] < val]
            elif op == "contains":
                df = df[df[col].astype(str).str.contains(str(val), na=False)]
            elif op == "in":
                df = df[df[col].isin(val)]
            elif op == "between":
                df = df[df[col].between(val[0], val[1])]
        return df

    # ----------------- Aggregation / Merge / Pivot -----------------
    def aggregate_data(self, data: pd.DataFrame, group_by: Union[str, List[str]], aggregations: Dict[str, Union[str, List[str]]]) -> pd.DataFrame:
        return data.groupby(group_by).agg(aggregations).reset_index()

    def merge_datasets(self, data1: pd.DataFrame, data2: pd.DataFrame, on: Optional[Union[str, List[str]]] = None, how: str = 'inner') -> pd.DataFrame:
        return pd.merge(data1, data2, on=on, how=how)

    def pivot_data(self, data: pd.DataFrame, index: Union[str, List[str]], columns: Union[str, List[str]], values: Union[str, List[str]], aggfunc: str = 'sum') -> pd.DataFrame:
        return pd.pivot_table(data, index=index, columns=columns, values=values, aggfunc=aggfunc).reset_index()

    # ----------------- Sorting / Sampling -----------------
    def sort_data(self, data: pd.DataFrame, columns: Union[str, List[str]], ascending: Union[bool, List[bool]] = True) -> pd.DataFrame:
        return data.sort_values(by=columns, ascending=ascending)

    def sample_data(self, data: pd.DataFrame, n: Optional[int] = None, frac: Optional[float] = None, random_state: int = 42) -> pd.DataFrame:
        return data.sample(n=n, frac=frac, random_state=random_state)

    # ----------------- Statistics -----------------
    def get_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        stats = {}
        numeric_cols = data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            stats[col] = {
                "count": int(data[col].count()),
                "mean": float(data[col].mean()),
                "median": float(data[col].median()),
                "std": float(data[col].std()),
                "min": float(data[col].min()),
                "max": float(data[col].max()),
                "quartiles": data[col].quantile([0.25, 0.5, 0.75]).to_dict()
            }
        return stats

    # ----------------- Type conversions -----------------
    def convert_data_types(self, data: pd.DataFrame, conversions: Dict[str, str]) -> pd.DataFrame:
        df = data.copy()
        for col, dtype in conversions.items():
            try:
                if dtype == 'datetime':
                    df[col] = pd.to_datetime(df[col])
                else:
                    df[col] = df[col].astype(dtype)
                if self.verbose:
                    print(f"Converted {col} to {dtype}")
            except Exception as e:
                print(f"Error converting {col} to {dtype}: {e}")
        return df

    # ----------------- Sample data -----------------
    def create_sample_data(self) -> pd.DataFrame:
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [25, 30, 35, 28, 32],
            'city': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney'],
            'salary': [50000, 60000, 75000, 55000, 65000],
            'department': ['IT', 'HR', 'IT', 'Finance', 'IT']
        })
        if self.verbose:
            print("Sample data created")
        return df


# ----------------- CLI -----------------
if __name__ == "__main__":
    processor = DataProcessor(verbose=True)

    if len(sys.argv) < 2:
        print("Usage: python data_processor.py <command> [args] [--preview n]")
        sys.exit(1)

    cmd = sys.argv[1]
    preview_rows = None

    # Check for preview flag
    if "--preview" in sys.argv:
        idx = sys.argv.index("--preview")
        if len(sys.argv) > idx + 1:
            preview_rows = int(sys.argv[idx + 1])

    def maybe_preview(df: pd.DataFrame):
        if preview_rows:
            print(f"\nPreviewing first {preview_rows} rows:")
            print(processor.preview_data(df, preview_rows))

    if cmd == "info":
        file_path = sys.argv[2]
        df = processor.read_data(file_path)
        maybe_preview(df)
        info = processor.get_data_info(df)
        print(f"\nDataset Information for {file_path}")
        print("="*40)
        print(f"Rows: {info['rows']}, Columns: {info['columns']}")
        print(f"Memory usage: {info['memory_usage']:,} bytes")
        print(f"Duplicates: {info['duplicates']}")
        print("\nNull counts per column:")
        for k, v in info['null_counts'].items():
            print(f" {k}: {v}")

    elif cmd == "clean":
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        df = processor.read_data(input_file)
        maybe_preview(df)
        cleaned = processor.clean_data(df)
        processor.write_data(cleaned, output_file)

    elif cmd == "convert":
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        fmt = sys.argv[4]
        df = processor.read_data(input_file)
        maybe_preview(df)
        processor.write_data(df, output_file, fmt)

    elif cmd == "stats":
        file_path = sys.argv[2]
        df = processor.read_data(file_path)
        maybe_preview(df)
        stats = processor.get_statistics(df)
        print(stats)

    elif cmd == "sample":
        file_path = sys.argv[2]
        n = int(sys.argv[3])
        df = processor.read_data(file_path)
        maybe_preview(df)
        sample = processor.sample_data(df, n=n)
        print(sample)

    elif cmd == "create_sample":
        df = processor.create_sample_data()
        maybe_preview(df)

    else:
        print(f"Unknown command: {cmd}")
