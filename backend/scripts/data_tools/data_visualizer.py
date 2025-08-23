import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

class DataVisualizer:
    def __init__(self):
        plt.style.use('default')
        sns.set_palette("husl")
    
    def load_data(self, file_path):
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                return pd.read_json(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                return pd.read_excel(file_path)
            else:
                print("Unsupported file format")
                return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def create_bar_chart(self, data, x_column, y_column, title="Bar Chart", output_file="bar_chart.png"):
        try:
            plt.figure(figsize=(10, 6))
            plt.bar(data[x_column], data[y_column])
            plt.title(title)
            plt.xlabel(x_column.replace('_', ' ').title())
            plt.ylabel(y_column.replace('_', ' ').title())
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Bar chart saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating bar chart: {e}")
            return False
    
    def create_line_chart(self, data, x_column, y_column, title="Line Chart", output_file="line_chart.png"):
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(data[x_column], data[y_column], marker='o')
            plt.title(title)
            plt.xlabel(x_column.replace('_', ' ').title())
            plt.ylabel(y_column.replace('_', ' ').title())
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Line chart saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating line chart: {e}")
            return False
    
    def create_pie_chart(self, data, column, title="Pie Chart", output_file="pie_chart.png"):
        try:
            plt.figure(figsize=(8, 8))
            value_counts = data[column].value_counts()
            plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            plt.title(title)
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Pie chart saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            return False
    
    def create_histogram(self, data, column, bins=20, title="Histogram", output_file="histogram.png"):
        try:
            plt.figure(figsize=(10, 6))
            plt.hist(data[column], bins=bins, alpha=0.7, edgecolor='black')
            plt.title(title)
            plt.xlabel(column.replace('_', ' ').title())
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Histogram saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating histogram: {e}")
            return False
    
    def create_scatter_plot(self, data, x_column, y_column, title="Scatter Plot", output_file="scatter_plot.png"):
        try:
            plt.figure(figsize=(10, 6))
            plt.scatter(data[x_column], data[y_column], alpha=0.6)
            plt.title(title)
            plt.xlabel(x_column.replace('_', ' ').title())
            plt.ylabel(y_column.replace('_', ' ').title())
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Scatter plot saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating scatter plot: {e}")
            return False
    
    def create_heatmap(self, data, title="Correlation Heatmap", output_file="heatmap.png"):
        try:
            numeric_data = data.select_dtypes(include=[np.number])
            if numeric_data.empty:
                print("No numeric columns found for heatmap")
                return False
            
            plt.figure(figsize=(10, 8))
            correlation_matrix = numeric_data.corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title(title)
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Heatmap saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            return False
    
    def create_box_plot(self, data, column, group_by=None, title="Box Plot", output_file="box_plot.png"):
        try:
            plt.figure(figsize=(10, 6))
            if group_by:
                data.boxplot(column=column, by=group_by)
                plt.suptitle('')
            else:
                plt.boxplot(data[column])
                plt.xticks([1], [column.replace('_', ' ').title()])
            
            plt.title(title)
            plt.ylabel(column.replace('_', ' ').title())
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Box plot saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating box plot: {e}")
            return False
    
    def create_dashboard(self, data, output_file="dashboard.png"):
        try:
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            categorical_columns = data.select_dtypes(include=['object']).columns
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Data Dashboard', fontsize=16)
            
            if len(numeric_columns) >= 1:
                axes[0, 0].hist(data[numeric_columns[0]], bins=20, alpha=0.7)
                axes[0, 0].set_title(f'Distribution of {numeric_columns[0]}')
                axes[0, 0].set_xlabel(numeric_columns[0])
                axes[0, 0].set_ylabel('Frequency')
            
            if len(categorical_columns) >= 1:
                value_counts = data[categorical_columns[0]].value_counts().head(10)
                axes[0, 1].bar(range(len(value_counts)), value_counts.values)
                axes[0, 1].set_title(f'Top Values in {categorical_columns[0]}')
                axes[0, 1].set_xticks(range(len(value_counts)))
                axes[0, 1].set_xticklabels(value_counts.index, rotation=45)
            
            if len(numeric_columns) >= 2:
                axes[1, 0].scatter(data[numeric_columns[0]], data[numeric_columns[1]], alpha=0.6)
                axes[1, 0].set_title(f'{numeric_columns[0]} vs {numeric_columns[1]}')
                axes[1, 0].set_xlabel(numeric_columns[0])
                axes[1, 0].set_ylabel(numeric_columns[1])
            
            if len(numeric_columns) >= 1:
                axes[1, 1].boxplot(data[numeric_columns[0]])
                axes[1, 1].set_title(f'Box Plot of {numeric_columns[0]}')
                axes[1, 1].set_ylabel(numeric_columns[0])
            
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            print(f"Dashboard saved as {output_file}")
            return True
        except Exception as e:
            print(f"Error creating dashboard: {e}")
            return False

def create_sample_data():
    np.random.seed(42)
    data = {
        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'sales': [100, 120, 140, 110, 160, 180],
        'profit': [20, 25, 30, 22, 35, 40],
        'category': ['A', 'B', 'A', 'C', 'B', 'A']
    }
    
    df = pd.DataFrame(data)
    df.to_csv('sample_viz_data.csv', index=False)
    print("Sample visualization data created: sample_viz_data.csv")

if __name__ == "__main__":
    visualizer = DataVisualizer()
    
    if len(sys.argv) < 2:
        print("Usage: python data_visualizer.py <command> [args]")
        print("Commands:")
        print("  bar <file> <x_col> <y_col>")
        print("  line <file> <x_col> <y_col>")
        print("  pie <file> <column>")
        print("  histogram <file> <column>")
        print("  scatter <file> <x_col> <y_col>")
        print("  heatmap <file>")
        print("  boxplot <file> <column>")
        print("  dashboard <file>")
        print("  create_sample")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create_sample":
        create_sample_data()
        sys.exit(0)
    
    if len(sys.argv) < 3:
        print("Please provide a data file")
        sys.exit(1)
    
    file_path = sys.argv[2]
    data = visualizer.load_data(file_path)
    
    if data is None:
        sys.exit(1)
    
    if command == "bar":
        if len(sys.argv) < 5:
            print("Usage: bar <file> <x_column> <y_column>")
            sys.exit(1)
        visualizer.create_bar_chart(data, sys.argv[3], sys.argv[4])
    
    elif command == "line":
        if len(sys.argv) < 5:
            print("Usage: line <file> <x_column> <y_column>")
            sys.exit(1)
        visualizer.create_line_chart(data, sys.argv[3], sys.argv[4])
    
    elif command == "pie":
        if len(sys.argv) < 4:
            print("Usage: pie <file> <column>")
            sys.exit(1)
        visualizer.create_pie_chart(data, sys.argv[3])
    
    elif command == "histogram":
        if len(sys.argv) < 4:
            print("Usage: histogram <file> <column>")
            sys.exit(1)
        visualizer.create_histogram(data, sys.argv[3])
    
    elif command == "scatter":
        if len(sys.argv) < 5:
            print("Usage: scatter <file> <x_column> <y_column>")
            sys.exit(1)
        visualizer.create_scatter_plot(data, sys.argv[3], sys.argv[4])
    
    elif command == "heatmap":
        visualizer.create_heatmap(data)
    
    elif command == "boxplot":
        if len(sys.argv) < 4:
            print("Usage: boxplot <file> <column>")
            sys.exit(1)
        visualizer.create_box_plot(data, sys.argv[3])
    
    elif command == "dashboard":
        visualizer.create_dashboard(data)
    
    else:
        print("Unknown command")
