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
    all_data = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(directory, file))
                all_data.append(df)
            except Exception as e:
                print(f"Error reading {file}: {e}")  # Explicitly print the error message
    if not all_data:
        raise ValueError("No valid CSV files found.")
    return pd.concat(all_data, ignore_index=True)

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

def main(args=None):
    parser = argparse.ArgumentParser(description="Stock Management Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Interactive mode
    subparsers.add_parser('interactive', help="Launch interactive menu")

    # Consolidate command
    consolidate_parser = subparsers.add_parser('consolidate', help="Consolidate CSV files")
    consolidate_parser.add_argument('--directory', required=True, help="Directory containing CSV files")

    # Search command
    search_parser = subparsers.add_parser('search', help="Search data in consolidated CSV")
    search_parser.add_argument('--directory', required=True, help="Directory containing CSV files")
    search_parser.add_argument('--column', required=True, help="Column to search")
    search_parser.add_argument('--value', required=True, help="Value to search for in the column")

    # Summary command
    summary_parser = subparsers.add_parser('summary', help="Generate summary report")
    summary_parser.add_argument('--directory', required=True, help="Directory containing CSV files")
    summary_parser.add_argument('--output', default=DEFAULT_REPORT_FILENAME, help="Output file for summary report")

    parsed_args = parser.parse_args(args)

    if parsed_args.command == 'interactive':
        interactive_menu()
    elif parsed_args.command == 'consolidate':
        try:
            df = consolidate_csv_files(parsed_args.directory)
            print("CSV files consolidated successfully.")
        except Exception as e:
            print(f"Error: {e}")
    elif parsed_args.command == 'search':
        try:
            df = consolidate_csv_files(parsed_args.directory)
            results = search_data(df, parsed_args.column, parsed_args.value)
            if results.empty:
                print("No matching records found.")
            else:
                print("Search Results:")
                print(results)
        except Exception as e:
            print(f"Error: {e}")
    elif parsed_args.command == 'summary':
        try:
            df = consolidate_csv_files(parsed_args.directory)
            generate_summary_report(df, parsed_args.output)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
