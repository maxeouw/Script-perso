import os
import pandas as pd
import unittest
from main import consolidate_csv_files, search_data, generate_summary_report

class TestStockManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set the directory containing the CSV files for testing."""
        cls.test_dir = os.path.join(os.path.dirname(__file__), "CSV")
        if not os.path.exists(cls.test_dir):
            raise FileNotFoundError(f"Test directory '{cls.test_dir}' does not exist.")

    def test_consolidate_csv_files(self):
        """Test consolidation of multiple CSV files."""
        df = consolidate_csv_files(self.test_dir)
        self.assertEqual(len(df), 12)  # Total rows from all files
        self.assertIn('category', df.columns)
        self.assertGreater(len(df), 0)  # Ensure DataFrame is not empty
        self.assertTrue(all(col in df.columns for col in ['name', 'quantity', 'price', 'category']))  # Check required columns
        self.assertEqual(df['category'].nunique(), 4)  # Ensure four unique categories
        self.assertFalse(df.isnull().values.any())  # Ensure no missing values

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

if __name__ == "__main__":
    unittest.main()
