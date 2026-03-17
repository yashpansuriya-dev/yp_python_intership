"""
Generate a small CSV file with random sample data.

Creates a file named `sample_data.csv` containing
10 rows of basic employee-style data.
"""

# -------------------------------------------------------------------

import csv
import random

# -------------------------------------------------------------------

# Sample values used to populate the CSV
NAMES = ["Yash", "Rahul", "Amit", "Priya", "Sneha", "Rohan"]
CITIES = ["Surat", "Ahmedabad", "Mumbai", "Delhi", "Pune"]


def generate_csv(file_name: str, rows: int = 10) -> None:
    """Create a CSV file with random records."""
    try:
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)

            # Write header row
            writer.writerow(["id", "name", "age", "city", "salary"])

            # Write random rows
            for i in range(rows):
                record = [
                    i + 1,
                    random.choice(NAMES),
                    random.randint(18, 40),
                    random.choice(CITIES),
                    random.randint(20000, 80000),
                ]
                writer.writerow(record)

    except PermissionError:
        print("Permission denied: unable to write file.")

    else:
        print("File created and written successfully.")

    finally:
        print("File operation completed.")

# -------------------------------------------------------------------

def main() -> None:
    generate_csv("Files/sample_data.csv")

    print("CSV file generated.")

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()