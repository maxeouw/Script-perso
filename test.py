import os
import pandas as pd
import unittest
from main import consolidate_csv_files, search_data, generate_summary_report, main
from unittest.mock import patch
import io
from argparse import Namespace

class TestStockManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set the directory containing the CSV files for testing."""
        cls.test_dir = os.path.join(os.path.dirname(__file__), "CSV")

    def test_consolidate_csv_files(self):
        """Test consolidation of multiple CSV files."""
        df = consolidate_csv_files(self.test_dir)
        self.assertEqual(len(df), 12)  # Total rows from all files
        self.assertIn('category', df.columns)
        self.assertGreater(len(df), 0)  # Ensure DataFrame is not empty
        self.assertTrue(all(col in df.columns for col in ['name', 'quantity', 'price', 'category']))  # Check required columns
        self.assertEqual(df['category'].nunique(), 4)  # Ensure four unique categories
        self.assertFalse(df.isnull().values.any())  # Ensure no missing values

    def test_consolidate_csv_files_no_csv_files(self):
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir, exist_ok=True)
        with self.assertRaises(ValueError):
            consolidate_csv_files(empty_dir)
        os.rmdir(empty_dir)

    def test_consolidate_csv_files_with_corrupted_file(self):
        """Test handling of corrupted CSV files during consolidation."""
        corrupted_file_path = os.path.join(self.test_dir, "corrupted.csv")

        try:
            # Create a corrupted CSV file
            with open(corrupted_file_path, "w") as f:
                f.write("name,quantity,price,category\n")
                f.write("item1,10,,Electronics\n")  # Missing price value
                f.write("item2,invalid_value,100,Furniture\n")  # Invalid quantity

            # Patch sys.stdout to capture printed output
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                # Attempt to consolidate files
                consolidate_csv_files(self.test_dir)
                output = mock_stdout.getvalue()

        finally:
            # Ensure the corrupted file is deleted
            if os.path.exists(corrupted_file_path):
                os.remove(corrupted_file_path)

    def test_search_data(self):
        """Test searching for data within a DataFrame."""
        df = consolidate_csv_files(self.test_dir)

        results = search_data(df, 'category', 'Electronics')
        self.assertEqual(len(results), 3)  # 3 rows in Electronics

        results = search_data(df, 'name', 'Table')
        self.assertEqual(len(results), 1)  # 1 row for Table

        results = search_data(df, 'name', 'Chair')
        self.assertEqual(len(results), 1)  # 1 row for Chair

        results = search_data(df, 'category', 'Furniture')
        self.assertEqual(len(results), 3)  # 3 rows in Furniture

        results = search_data(df, 'name', 'Nonexistent')
        self.assertEqual(len(results), 0)  # No rows for non-existent item

        sample_data = pd.DataFrame({
            "name": ["item1", "item2", "item3"],
            "quantity": [10, 20, 30],
            "price": [100.0, 200.0, 300.0],
            "category": ["Electronics", "Furniture", "Electronics"]
        })

        with patch("main.consolidate_csv_files", return_value=sample_data), \
                patch("builtins.input", side_effect=["1", self.test_dir, "2", "category", "Electronics", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()

        # Check that the search results are printed
        self.assertIn("Search Results:", output)
        self.assertIn("category", output)  # Ensure results contain the 'category' column
        self.assertIn("Electronics", output)  # Ensure results contain the searched value

    def test_search_data_column_not_found(self):
        df = pd.DataFrame({"name": ["item1", "item2"], "quantity": [10, 20]})
        with self.assertRaises(KeyError):
            search_data(df, "nonexistent_column", "item")

    def test_generate_summary_report(self):
        """Test generation of a summary report."""
        df = consolidate_csv_files(self.test_dir)
        output_file = os.path.join(self.test_dir, 'summary_report.csv')

        generate_summary_report(df, output_file)

        # Verify that the summary report was created
        self.assertTrue(os.path.exists(output_file))

        # Load the report and validate its content
        summary = pd.read_csv(output_file)
        self.assertIn('category', summary.columns)
        self.assertIn('Total Quantity', summary.columns)
        self.assertIn('Average Price', summary.columns)

        # Check specific summary values for a category
        electronics_summary = summary[summary['category'] == 'Electronics']
        self.assertEqual(electronics_summary['Total Quantity'].values[0], 245)
        self.assertAlmostEqual(electronics_summary['Average Price'].values[0], 699.99, places=2)

        # Additional test cases
        self.assertEqual(len(summary), 4)  # 4 categories in summary
        self.assertTrue((summary['Total Quantity'] > 0).all())  # Ensure positive quantities
        self.assertTrue((summary['Average Price'] > 0).all())  # Ensure positive prices
        self.assertTrue(summary['category'].is_unique)  # Ensure unique categories in summary

        # Cleanup: Remove the summary report file
        if os.path.exists(output_file):
            os.remove(output_file)

    def test_generate_summary_report_missing_columns(self):
        """Test summary report generation with missing required columns."""
        df = pd.DataFrame({
            "name": ["item1", "item2"],
            "quantity": [10, 20]
            # Missing 'category' and 'price' columns
        })
        output_file = os.path.join(self.test_dir, 'summary_report_missing.csv')

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            generate_summary_report(df, output_file)
            output = mock_stdout.getvalue()
            self.assertIn("Missing required column in data", output)

        # Ensure the report file was not created
        self.assertFalse(os.path.exists(output_file))

    def test_invalid_directory(self):
        """Test handling of an invalid directory in the interactive menu."""
        with patch("builtins.input", side_effect=["1", "invalid_directory", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()
            self.assertIn("Invalid directory. Please try again.", output)

    def test_error_during_consolidation(self):
        """Test error handling during CSV consolidation."""
        with patch("main.consolidate_csv_files", side_effect=Exception("Mocked error")), \
                patch("builtins.input", side_effect=["1", self.test_dir, "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()
            self.assertIn("Error: Mocked error", output)

    def test_no_data_available(self):
        """Test error messages when no data is consolidated."""
        with patch("builtins.input", side_effect=["2", "3", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()
            self.assertIn("No data available. Please consolidate CSV files first.", output)

    def test_search_with_invalid_column(self):
        """Test searching with an invalid column."""
        df = consolidate_csv_files(self.test_dir)
        with patch("main.consolidate_csv_files", return_value=df), \
                patch("builtins.input", side_effect=["1", self.test_dir, "2", "invalid_column", "value", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()
            self.assertIn("Column 'invalid_column' not found in the DataFrame.",
                          output)  # Updated to match actual message

    def test_search_no_results(self):
        """Test searching with no matching results."""
        df = consolidate_csv_files(self.test_dir)
        with patch("main.consolidate_csv_files", return_value=df), \
                patch("builtins.input", side_effect=["1", self.test_dir, "2", "category", "Nonexistent", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()
            self.assertIn("No matching records found.", output)

    def test_invalid_choice(self):
        """Test invalid choice in the interactive menu."""
        with patch("builtins.input", side_effect=["5", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()
            self.assertIn("Invalid choice. Please try again.", output)

    def test_main_interactive_mode(self):
        """Test main function in interactive mode."""
        with patch("builtins.input", side_effect=["1", self.test_dir, "3", "", "4"]), \
             patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()
            self.assertIn("CSV files consolidated successfully.", output)

    def test_main_consolidate_command(self):
        """Test consolidate command with argparse."""
        args = ["consolidate", "--directory", self.test_dir]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(args)
            output = mock_stdout.getvalue()
            self.assertIn("CSV files consolidated successfully.", output)

        with patch("main.consolidate_csv_files", side_effect=Exception("Mocked consolidation error")), \
                patch("builtins.input", side_effect=["1", self.test_dir, "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()

        self.assertIn("Error: Mocked consolidation error", output)  # Check for error message

        with patch("main.consolidate_csv_files", return_value=pd.DataFrame()), \
                patch("main.search_data", side_effect=Exception("Mocked search error")), \
                patch("builtins.input", side_effect=["1", self.test_dir, "2", "category", "value", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()

        self.assertIn("Error: Mocked search error", output)  # Check for error message

    def test_main_search_command(self):
        """Test search command with argparse."""
        df = consolidate_csv_files(self.test_dir)
        with patch("main.consolidate_csv_files", return_value=df):
            args = ["search", "--directory", self.test_dir, "--column", "category", "--value", "Electronics"]
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main(args)
                output = mock_stdout.getvalue()
                self.assertIn("Search Results:", output)

    def test_main_summary_command(self):
        """Test summary report generation with argparse."""
        args = ["summary", "--directory", self.test_dir, "--output", "custom_report.csv"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(args)
            output = mock_stdout.getvalue()
            self.assertIn("Summary report saved to custom_report.csv", output)
            os.remove("custom_report.csv")

    def test_no_matching_records(self):
        """Test handling of no matching records during search."""
        with patch("main.consolidate_csv_files", return_value=pd.DataFrame({
            "name": ["item1", "item2"],
            "quantity": [10, 20],
            "category": ["Electronics", "Furniture"]
        })), \
                patch("builtins.input", side_effect=["1", self.test_dir, "2", "name", "nonexistent", "4"]), \
                patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main(["interactive"])
            output = mock_stdout.getvalue()

        self.assertIn("No matching records found.", output)


if __name__ == "__main__":
    unittest.main()
