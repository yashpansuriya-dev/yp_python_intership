import csv
import tempfile
import unittest
from pathlib import Path

from my_actor.main import category_page_url, slugify, write_csv_outputs


class CsvExportTests(unittest.TestCase):
    def test_slugify_names_for_folders_and_files(self):
        self.assertEqual(slugify("Application Development"), "application_development")
        self.assertEqual(slugify("Jira Software!"), "jira_software")
        self.assertEqual(slugify(""), "item")

    def test_category_page_url_adds_pagination_query(self):
        start_url = "https://www.capterra.com/application-development-software/"

        self.assertEqual(category_page_url(start_url, 1), start_url)
        self.assertEqual(
            category_page_url(start_url, 2),
            "https://www.capterra.com/application-development-software/?page=2",
        )
        self.assertEqual(
            category_page_url("https://www.capterra.com/application-development-software/?page=5", 6),
            "https://www.capterra.com/application-development-software/?page=6",
        )

    def test_write_csv_outputs_splits_products_and_reviews(self):
        products = [
            {
                "name": "Wix",
                "url": "https://example.com/wix",
                "rating": "4.4",
                "reviews_count": "100",
                "description": "Website builder",
                "reviews": [
                    {
                        "review_title": "Easy to use",
                        "review_description": "Simple editor",
                        "author_name": "Alex",
                        "review_stars": "5",
                        "review_date": "April 1, 2026",
                        "review_pros": "Fast setup",
                        "review_cons": "Limited export",
                    }
                ],
            },
            {
                "name": "Jira Software",
                "url": "https://example.com/jira",
                "rating": "4.3",
                "reviews_count": "200",
                "description": "Issue tracking",
                "reviews": [],
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = write_csv_outputs(
                "Application Development",
                products,
                base_dir=Path(temp_dir),
                batch_label="from_page_5_limit_100",
            )

            self.assertEqual(output_dir.name, "application_development")
            self.assertTrue((output_dir / "products.csv").exists())
            self.assertTrue((output_dir / "00_application_development_products.csv").exists())
            self.assertTrue((output_dir / "00_application_development_products_from_page_5_limit_100.csv").exists())
            self.assertTrue((output_dir / "wix_reviews.csv").exists())
            self.assertTrue((output_dir / "jira_software_reviews.csv").exists())

            with (output_dir / "products.csv").open(newline="", encoding="utf-8-sig") as csv_file:
                product_rows = list(csv.DictReader(csv_file))

            self.assertEqual(product_rows[0]["product_index"], "1")
            self.assertEqual(product_rows[0]["product_id"], "wix")
            self.assertEqual(product_rows[0]["software_category"], "Application Development")
            self.assertEqual(product_rows[1]["product_index"], "2")
            self.assertEqual(product_rows[1]["product_id"], "jira_software")

            with (output_dir / "wix_reviews.csv").open(newline="", encoding="utf-8-sig") as csv_file:
                review_rows = list(csv.DictReader(csv_file))

            self.assertEqual(review_rows[0]["product_id"], "wix")
            self.assertEqual(review_rows[0]["review_title"], "Easy to use")
            self.assertEqual(review_rows[0]["description"], "Simple editor")
            self.assertEqual(review_rows[0]["author"], "Alex")
            self.assertEqual(review_rows[0]["rating"], "5")
            self.assertEqual(review_rows[0]["date"], "April 1, 2026")

    def test_write_csv_outputs_appends_to_existing_category_folder(self):
        first_batch = [
            {
                "name": "Wix",
                "url": "https://example.com/wix",
                "rating": "4.4",
                "reviews_count": "100",
                "description": "Website builder",
                "reviews": [],
            },
        ]
        second_batch = [
            {
                "name": "Wix",
                "url": "https://example.com/wix",
                "rating": "4.4",
                "reviews_count": "100",
                "description": "Duplicate should be skipped",
                "reviews": [],
            },
            {
                "name": "Jira",
                "url": "https://example.com/jira",
                "rating": "4.3",
                "reviews_count": "200",
                "description": "Issue tracking",
                "reviews": [],
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = write_csv_outputs("Application Development", first_batch, base_dir=Path(temp_dir))
            output_dir = write_csv_outputs("Application Development", second_batch, base_dir=Path(temp_dir))

            with (output_dir / "products.csv").open(newline="", encoding="utf-8-sig") as csv_file:
                product_rows = list(csv.DictReader(csv_file))

            self.assertEqual([row["product_id"] for row in product_rows], ["wix", "jira"])
            self.assertEqual([row["product_index"] for row in product_rows], ["1", "2"])
            self.assertTrue((output_dir / "00_application_development_products.csv").exists())
            self.assertTrue((output_dir / "wix_reviews.csv").exists())
            self.assertTrue((output_dir / "jira_reviews.csv").exists())


if __name__ == "__main__":
    unittest.main()
