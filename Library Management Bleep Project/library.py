# library.py
# Library manager class - keeps all books and handles the csv file.

import csv
import os

from book import Book, book_from_row

FIELDS = ["book_id", "title", "author", "genre", "year",
          "status", "issued_to", "issue_date", "due_date"]


class Library:
    def __init__(self, filename="books.csv"):
        folder = os.path.dirname(os.path.abspath(__file__))
        self.file = os.path.join(folder, filename)
        self.books = {}        # book_id -> Book

    # ---- helpers ----
    def next_id(self):
        numbers = []
        for b in self.books:
            if b[1:].isdigit():
                numbers.append(int(b[1:]))
        if len(numbers) == 0:
            return "B101"
        return "B" + str(max(numbers) + 1)

    def get_book(self, book_id):
        book_id = str(book_id).strip().upper()
        if book_id not in self.books:
            raise Exception("No book found with ID " + book_id)
        return self.books[book_id]

    # ---- features ----
    def add_book(self, title, author, genre, year):
        book = Book(self.next_id(), title, author, genre, year)
        for existing in self.books.values():
            if existing.get_title().lower() == book.get_title().lower() and \
               existing.get_author().lower() == book.get_author().lower():
                raise Exception("'" + existing.get_title() + "' by " + existing.get_author() +
                                " already exists (ID " + existing.get_item_id() + ")")
        self.books[book.get_item_id()] = book
        return book

    def all_books(self):
        result = list(self.books.values())
        result.sort(key=lambda b: b.get_item_id())
        return result

    def available_books(self):
        result = []
        for b in self.all_books():
            if b.is_available():
                result.append(b)
        return result

    def search(self, keyword):
        # try 'available', 'issued' or 'overdue' to list books by status
        keyword = str(keyword).strip().lower()
        if keyword == "":
            return []
        results = []
        for b in self.all_books():
            status_word = "available" if b.is_available() else "issued"
            searchable = " ".join([b.get_item_id(), b.get_title(), b.get_author(),
                                   b.get_genre(), status_word,
                                   b.get_issued_to() or "", b.status_text()]).lower()
            if keyword in searchable:
                results.append(b)
        return results

    def issue_book(self, book_id, member):
        book = self.get_book(book_id)
        book.issue(member)
        return book

    def return_book(self, book_id):
        book = self.get_book(book_id)
        overdue = book.return_book()
        return book, overdue

    # ---- file handling ----
    def load_data(self):
        messages = []
        if not os.path.exists(self.file):
            messages.append("books.csv not found - starting with no records.")
            return messages

        try:
            f = open(self.file, newline="", encoding="utf-8")
        except OSError as e:
            messages.append("Could not read books file: " + str(e))
            return messages

        line_no = 1
        for row in csv.DictReader(f):
            line_no += 1
            try:
                book = book_from_row(row)
                if book.get_item_id() in self.books:
                    raise Exception("duplicate ID " + book.get_item_id())
                self.books[book.get_item_id()] = book
            except (ValueError, Exception) as e:
                messages.append("Skipped line " + str(line_no) + " in books.csv: " + str(e))
        f.close()
        return messages

    def save_data(self):
        try:
            f = open(self.file, "w", newline="", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(FIELDS)
            for book in self.all_books():
                writer.writerow(book.to_row())
            f.close()
            return True
        except OSError as e:
            print("Error: could not save records (" + str(e) + ")")
            return False
