import argparse
import os
import pandas as pd

DEFAULT_REPORT_FILENAME = "report.csv"

def consolidate_csv_files(directory: str) -> pd.DataFrame:
    """
    Consolidate all CSV files in the specified directory into a single DataFrame.

    Raises:
        ValueError: If no CSV files are found in the directory.
    """
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    if not csv_files:
        raise ValueError("No CSV files found in the directory.")

    dataframes = []
    for file in csv_files:
        file_path = os.path.join(directory, file)
        try:
            df = pd.read_csv(file_path)
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    return pd.concat(dataframes, ignore_index=True)

def search_data(dataframe: pd.DataFrame, column: str, search_value: str) -> pd.DataFrame:
    """
    Search for rows in the DataFrame where the specified column contains the search value.

    Raises:
        KeyError: If the column does not exist in the DataFrame.
    """
    if column not in dataframe.columns:
        raise KeyError(f"Column '{column}' not found in the DataFrame.")

    return dataframe[dataframe[column].astype(str) == search_value]

def generate_summary_report(dataframe: pd.DataFrame, output_file: str = DEFAULT_REPORT_FILENAME) -> None:
    """
    Generate a summary report grouped by category, showing total quantity and average price.

    Raises:
        KeyError: If required columns are missing in the DataFrame.
    """
    try:
        summary = dataframe.groupby('category').agg({
            'quantity': 'sum',
            'price': 'mean'
        }).rename(columns={
            'quantity': 'Total Quantity',
            'price': 'Average Price'
        })
        summary['Average Price'] = summary['Average Price'].round(2)
        summary.to_csv(output_file)
        print(f"Summary report saved to {output_file}")
    except KeyError as e:
        print(f"Missing required column in data: {e}")
    except Exception as e:
        print(f"Error generating summary report: {e}")

def interactive_menu() -> None:
    """
    Interactive menu for the Stock Management Tool.
    """
    print("Welcome to the Stock Management Tool")
    print("1. Consolidate CSV Files")
    print("2. Search Data")
    print("3. Generate Summary Report")
    print("4. Exit")

    data = None

    while True:
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            directory = input("Enter the directory containing CSV files: ").strip()
            if not os.path.isdir(directory):
                print("Invalid directory. Please try again.")
                continue
            try:
                data = consolidate_csv_files(directory)
                print("CSV files consolidated successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '2':
            if data is None:
                print("No data available. Please consolidate CSV files first.")
                continue

            column = input("Enter the column to search: ").strip()
            search_value = input("Enter the search value: ").strip()
            try:
                results = search_data(data, column, search_value)
                if results.empty:
                    print("No matching records found.")
                else:
                    print("Search Results:")
                    print(results)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            if data is None:
                print("No data available. Please consolidate CSV files first.")
                continue

            output_file = input("Enter the output file name for the summary report (or press Enter for default): ").strip()
            output_file = output_file if output_file else DEFAULT_REPORT_FILENAME
            generate_summary_report(data, output_file)

        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="Stock Management Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('interactive', help="Launch interactive menu")

    args = parser.parse_args()

    if args.command == 'interactive':
        interactive_menu()

if __name__ == "__main__":
    main()
