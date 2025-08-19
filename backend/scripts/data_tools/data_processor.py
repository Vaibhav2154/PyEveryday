import pandas as pd
import json
import csv
import sys
import os

class DataProcessor:
    def __init__(self):
        self.supported_formats = ['csv', 'json', 'excel', 'txt']
    
    def read_data(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.csv':
                return pd.read_csv(file_path)
            elif file_ext == '.json':
                return pd.read_json(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            elif file_ext == '.txt':
                return pd.read_csv(file_path, delimiter='\t')
            else:
                print(f"Unsupported file format: {file_ext}")
                return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def write_data(self, data, file_path, format_type=None):
        if format_type is None:
            format_type = os.path.splitext(file_path)[1].lower()[1:]
        
        try:
            if format_type == 'csv':
                data.to_csv(file_path, index=False)
            elif format_type == 'json':
                data.to_json(file_path, orient='records', indent=2)
            elif format_type in ['xlsx', 'excel']:
                data.to_excel(file_path, index=False)
            else:
                print(f"Unsupported output format: {format_type}")
                return False
            
            print(f"Data saved to {file_path}")
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    def get_data_info(self, data):
        info = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.to_dict(),
            'null_counts': data.isnull().sum().to_dict(),
            'memory_usage': data.memory_usage(deep=True).sum(),
            'duplicates': data.duplicated().sum()
        }
        return info
    
    def clean_data(self, data, operations=None):
        if operations is None:
            operations = ['remove_duplicates', 'fill_nulls', 'strip_strings']
        
        cleaned_data = data.copy()
        
        if 'remove_duplicates' in operations:
            cleaned_data = cleaned_data.drop_duplicates()
            print(f"Removed {len(data) - len(cleaned_data)} duplicate rows")
        
        if 'fill_nulls' in operations:
            for column in cleaned_data.columns:
                if cleaned_data[column].dtype == 'object':
                    cleaned_data[column].fillna('Unknown', inplace=True)
                else:
                    cleaned_data[column].fillna(cleaned_data[column].mean(), inplace=True)
            print("Filled null values")
        
        if 'strip_strings' in operations:
            for column in cleaned_data.select_dtypes(include=['object']).columns:
                cleaned_data[column] = cleaned_data[column].astype(str).str.strip()
            print("Stripped whitespace from string columns")
        
        return cleaned_data
    
    def filter_data(self, data, conditions):
        filtered_data = data.copy()
        
        for condition in conditions:
            column = condition['column']
            operator = condition['operator']
            value = condition['value']
            
            if operator == 'equals':
                filtered_data = filtered_data[filtered_data[column] == value]
            elif operator == 'not_equals':
                filtered_data = filtered_data[filtered_data[column] != value]
            elif operator == 'greater_than':
                filtered_data = filtered_data[filtered_data[column] > value]
            elif operator == 'less_than':
                filtered_data = filtered_data[filtered_data[column] < value]
            elif operator == 'contains':
                filtered_data = filtered_data[filtered_data[column].str.contains(str(value), na=False)]
        
        return filtered_data
    
    def aggregate_data(self, data, group_by, aggregations):
        try:
            grouped = data.groupby(group_by)
            result = grouped.agg(aggregations).reset_index()
            return result
        except Exception as e:
            print(f"Error aggregating data: {e}")
            return None
    
    def merge_datasets(self, data1, data2, on=None, how='inner'):
        try:
            merged = pd.merge(data1, data2, on=on, how=how)
            return merged
        except Exception as e:
            print(f"Error merging datasets: {e}")
            return None
    
    def pivot_data(self, data, index, columns, values, aggfunc='sum'):
        try:
            pivoted = data.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc)
            return pivoted.reset_index()
        except Exception as e:
            print(f"Error pivoting data: {e}")
            return None
    
    def sort_data(self, data, columns, ascending=True):
        try:
            if isinstance(columns, str):
                columns = [columns]
            if isinstance(ascending, bool):
                ascending = [ascending] * len(columns)
            
            sorted_data = data.sort_values(by=columns, ascending=ascending)
            return sorted_data
        except Exception as e:
            print(f"Error sorting data: {e}")
            return None
    
    def sample_data(self, data, n=None, frac=None, random_state=42):
        try:
            if n is not None:
                return data.sample(n=n, random_state=random_state)
            elif frac is not None:
                return data.sample(frac=frac, random_state=random_state)
            else:
                return data.head(10)
        except Exception as e:
            print(f"Error sampling data: {e}")
            return None
    
    def get_statistics(self, data):
        numeric_columns = data.select_dtypes(include=['number']).columns
        
        stats = {}
        for column in numeric_columns:
            stats[column] = {
                'count': data[column].count(),
                'mean': data[column].mean(),
                'median': data[column].median(),
                'std': data[column].std(),
                'min': data[column].min(),
                'max': data[column].max(),
                'quartiles': data[column].quantile([0.25, 0.5, 0.75]).to_dict()
            }
        
        return stats
    
    def convert_data_types(self, data, conversions):
        converted_data = data.copy()
        
        for column, new_type in conversions.items():
            try:
                if new_type == 'datetime':
                    converted_data[column] = pd.to_datetime(converted_data[column])
                else:
                    converted_data[column] = converted_data[column].astype(new_type)
                print(f"Converted {column} to {new_type}")
            except Exception as e:
                print(f"Error converting {column} to {new_type}: {e}")
        
        return converted_data

def create_sample_data():
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'city': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney'],
        'salary': [50000, 60000, 75000, 55000, 65000],
        'department': ['IT', 'HR', 'IT', 'Finance', 'IT']
    }
    
    df = pd.DataFrame(data)
    df.to_csv('sample_data.csv', index=False)
    print("Sample data created: sample_data.csv")

if __name__ == "__main__":
    processor = DataProcessor()
    
    if len(sys.argv) < 2:
        print("Usage: python data_processor.py <command> [args]")
        print("Commands:")
        print("  info <file>                    - Get data information")
        print("  clean <file> <output>          - Clean data")
        print("  convert <file> <output> <format> - Convert format")
        print("  stats <file>                   - Get statistics")
        print("  sample <file> <n>              - Sample data")
        print("  create_sample                  - Create sample CSV file")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "info":
        if len(sys.argv) < 3:
            print("Usage: info <file>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        data = processor.read_data(file_path)
        
        if data is not None:
            info = processor.get_data_info(data)
            print(f"\nDataset Information for {file_path}")
            print("="*40)
            print(f"Shape: {info['shape'][0]} rows, {info['shape'][1]} columns")
            print(f"Columns: {', '.join(info['columns'])}")
            print(f"Memory usage: {info['memory_usage']:,} bytes")
            print(f"Duplicates: {info['duplicates']}")
            print("\nNull values per column:")
            for col, nulls in info['null_counts'].items():
                if nulls > 0:
                    print(f"  {col}: {nulls}")
    
    elif command == "clean":
        if len(sys.argv) < 4:
            print("Usage: clean <input_file> <output_file>")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        data = processor.read_data(input_file)
        if data is not None:
            cleaned_data = processor.clean_data(data)
            processor.write_data(cleaned_data, output_file)
    
    elif command == "convert":
        if len(sys.argv) < 5:
            print("Usage: convert <input_file> <output_file> <format>")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        output_format = sys.argv[4]
        
        data = processor.read_data(input_file)
        if data is not None:
            processor.write_data(data, output_file, output_format)
    
    elif command == "stats":
        if len(sys.argv) < 3:
            print("Usage: stats <file>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        data = processor.read_data(file_path)
        
        if data is not None:
            stats = processor.get_statistics(data)
            print(f"\nStatistics for {file_path}")
            print("="*40)
            
            for column, column_stats in stats.items():
                print(f"\n{column}:")
                print(f"  Count: {column_stats['count']}")
                print(f"  Mean: {column_stats['mean']:.2f}")
                print(f"  Median: {column_stats['median']:.2f}")
                print(f"  Std Dev: {column_stats['std']:.2f}")
                print(f"  Min: {column_stats['min']:.2f}")
                print(f"  Max: {column_stats['max']:.2f}")
    
    elif command == "sample":
        if len(sys.argv) < 4:
            print("Usage: sample <file> <n>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        n = int(sys.argv[3])
        
        data = processor.read_data(file_path)
        if data is not None:
            sample_data = processor.sample_data(data, n=n)
            print(f"\nSample of {n} rows from {file_path}")
            print("="*40)
            print(sample_data.to_string(index=False))
    
    elif command == "create_sample":
        create_sample_data()
    
    else:
        print("Unknown command")
