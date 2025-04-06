import csv
import os
from django.core.management.base import BaseCommand
from books.models import Book, Category
from django.utils.dateparse import parse_date
from datetime import datetime

class Command(BaseCommand):
    help = 'Import books data from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = r'C:\Users\nikol\Desktop\coursera\ExpenseTrackerDjango\Books Distribution Expenses - Books.csv'  # Adjust path if needed

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Check if the category exists or create it
                    category_name = row['category'].strip()
                    category, created = Category.objects.get_or_create(name=category_name)

                    # Handle missing or invalid published_date
                    published_date_str = row['published_date'].strip()

                    if published_date_str:
                        # Convert MM/DD/YYYY to YYYY-MM-DD
                        try:
                            published_date = datetime.strptime(published_date_str, "%m/%d/%Y").date()
                        except ValueError:
                            # Log the error and set a default date if the format is wrong
                            self.stdout.write(self.style.WARNING(f"Invalid date format for book '{row['title']}': {published_date_str}. Using default date."))
                            published_date = datetime(2000, 1, 1).date()
                    else:
                        # If no date, set it to a default date
                        published_date = datetime(2000, 1, 1).date()

                    # Create the book entry
                    book = Book(
                        title=row['title'],
                        subtitle=row['subtitle'],
                        authors=row['authors'],
                        publisher=row['publisher'],
                        published_date=published_date,  # Valid date
                        category=category,
                        distribution_expense=row['distribution_expense'],
                    )
                    book.save()

                self.stdout.write(self.style.SUCCESS('Successfully imported books from CSV'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing CSV: {e}'))
