import os
import pandas as pd


def consolidate_csv_files(directory):
    """
    Consolidate all CSV files in the specified directory into a single DataFrame.
    """
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    dataframes = []

    for file in csv_files:
        file_path = os.path.join(directory, file)
        try:
            df = pd.read_csv(file_path)
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    else:
        raise ValueError("No CSV files found in the directory.")


def search_data(dataframe, column, search_value):
    """
    Search for rows in the DataFrame where the specified column contains the search value.
    """
    if column not in dataframe.columns:
        raise KeyError(f"Column '{column}' not found in the DataFrame.")

    return dataframe[dataframe[column].astype(str).str.contains(search_value, case=False, na=False)]


def generate_summary_report(dataframe, output_file):
    """
    Generate a summary report grouped by category, showing total quantity and average price.
    """
    try:
        summary = dataframe.groupby('category').agg({
            'quantity': 'sum',
            'price': 'mean'
        }).rename(columns={
            'quantity': 'Total Quantity',
            'price': 'Average Price'
        })
        summary.to_csv(output_file)
        print(f"Summary report saved to {output_file}")
    except KeyError as e:
        print(f"Missing required column in data: {e}")
    except Exception as e:
        print(f"Error generating summary report: {e}")


def main():
    """
    Main function to provide a command-line interface for the stock management tool.
    """
    print("Welcome to the Stock Management Tool")
    print("1. Consolidate CSV Files")
    print("2. Search Data")
    print("3. Generate Summary Report")
    print("4. Exit")

    data = None

    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            directory = input("Enter the directory containing CSV files: ")
            try:
                data = consolidate_csv_files(directory)
                print("CSV files consolidated successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '2':
            if data is None:
                print("No data available. Please consolidate CSV files first.")
                continue

            column = input("Enter the column to search: ")
            search_value = input("Enter the search value: ")
            try:
                results = search_data(data, column, search_value)
                print("Search Results:")
                print(results)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            if data is None:
                print("No data available. Please consolidate CSV files first.")
                continue

            output_file = input("Enter the output file name for the summary report: ")
            generate_summary_report(data, output_file)

        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
