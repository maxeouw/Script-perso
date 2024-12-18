import os
import pandas as pd
import unittest
from main import consolidate_csv_files, search_data, generate_summary_report, main, DEFAULT_REPORT_FILENAME
from unittest.mock import patch
import io

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

    def test_main_menu_display(self):
        with patch("builtins.input", side_effect=["4"]), patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Welcome to the Stock Management Tool", output)
            self.assertIn("1. Consolidate CSV Files", output)
            self.assertIn("4. Exit", output)

    def test_main_invalid_choice(self):
        with patch("builtins.input", side_effect=["invalid", "4"]), patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Invalid choice. Please try again.", output)

    def test_main_exit(self):
        with patch("builtins.input", side_effect=["4"]), patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Exiting the program. Goodbye!", output)

    def test_main_consolidate_valid_directory(self):
        with patch("builtins.input", side_effect=["1", self.test_dir, "4"]), patch("sys.stdout",
                                                                                   new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("CSV files consolidated successfully.", output)

    def test_main_consolidate_invalid_directory(self):
        with patch("builtins.input", side_effect=["1", "invalid_directory", "4"]), patch("sys.stdout",
                                                                                         new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Invalid directory. Please try again.", output)

    def test_main_search_success(self):
        with patch("builtins.input", side_effect=["1", self.test_dir, "2", "category", "Electronics", "4"]), patch(
                "sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Search Results:", output)

    def test_main_search_no_results(self):
        with patch("builtins.input", side_effect=["1", self.test_dir, "2", "name", "Nonexistent", "4"]), patch(
                "sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No matching records found.", output)

    def test_main_search_invalid_column(self):
        with patch("builtins.input", side_effect=["1", self.test_dir, "2", "invalid_column", "value", "4"]), patch(
                "sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Error:", output)

    def test_main_generate_report_custom_file(self):
        with patch("builtins.input", side_effect=["1", self.test_dir, "3", "custom_report.csv", "4"]), patch(
                "sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Summary report saved to custom_report.csv", output)
            os.remove("custom_report.csv")  # Cleanup

    def test_main_generate_report_default_file(self):
        with patch("builtins.input", side_effect=["1", self.test_dir, "3", "", "4"]), patch("sys.stdout",
                                                                                            new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn(f"Summary report saved to {DEFAULT_REPORT_FILENAME}", output)
            os.remove(DEFAULT_REPORT_FILENAME)  # Cleanup

    def test_main_generate_report_no_data(self):
        with patch("builtins.input", side_effect=["3", "4"]), patch("sys.stdout",
                                                                    new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No data available. Please consolidate CSV files first.", output)

    def test_main_no_data_for_search(self):
        with patch("builtins.input", side_effect=["2", "4"]), patch("sys.stdout",
                                                                    new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No data available. Please consolidate CSV files first.", output)

    def test_main_no_data_for_report(self):
        with patch("builtins.input", side_effect=["3", "4"]), patch("sys.stdout",
                                                                    new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No data available. Please consolidate CSV files first.", output)

    def test_main_program_execution(self):
        with patch("builtins.input", side_effect=["1", self.test_dir, "4"]), patch("sys.stdout",
                                                                                   new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Welcome to the Stock Management Tool", output)
            self.assertIn("CSV files consolidated successfully.", output)
            self.assertIn("Exiting the program. Goodbye!", output)

if __name__ == "__main__":
    unittest.main()
