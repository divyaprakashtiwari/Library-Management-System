# main.py
# Library Management System - menu driven console program

from library import Library
from book import validate_title, validate_author, validate_genre, validate_year, validate_member

MENU = """
========== LIBRARY MANAGEMENT SYSTEM ==========
1. Add book
2. Search books
3. Issue book
4. Return book
5. Display available books
6. Save records
7. Save and exit
===============================================
"""


def ask(prompt, validate_func):
    while True:
        value = input(prompt)
        try:
            return validate_func(value)
        except ValueError as e:
            print("  Invalid input:", e)


def trunc(text, width):
    if len(text) <= width:
        return text
    return text[:width - 2] + ".."


def print_table(books, show_status):
    header = "ID".ljust(6) + "Title".ljust(41) + "Author".ljust(27) + "Genre".ljust(14) + "Year".ljust(5)
    if show_status:
        header = header + "Status"
    print(header)
    print("-" * (len(header) + (14 if show_status else 0)))
    for b in books:
        row = (b.get_item_id().ljust(6) + trunc(b.get_title(), 40).ljust(41) +
               trunc(b.get_author(), 26).ljust(27) + trunc(b.get_genre(), 13).ljust(14) +
               str(b.get_year()).ljust(5))
        if show_status:
            row = row + b.status_text()
        print(row)


def add_book(library):
    title = ask("Book title: ", validate_title)
    author = ask("Author: ", validate_author)
    genre = ask("Genre: ", validate_genre)
    year = ask("Year of publication: ", validate_year)
    book = library.add_book(title, author, genre, year)
    print("Book added successfully with ID", book.get_item_id())


def search_books(library):
    keyword = input("Search by ID, title, author, genre, member, or 'available'/'issued'/'overdue': ")
    results = library.search(keyword)
    if len(results) == 0:
        print("No matching books found.")
        return
    print()
    print_table(results, show_status=True)
    print("\n" + str(len(results)) + " book(s) found.")


def issue_book(library):
    book = library.get_book(input("Enter book ID to issue: "))
    if not book.is_available():
        raise Exception("'" + book.get_title() + "' is already issued to " + book.get_issued_to() +
                        " (due " + book.get_due_date().strftime("%d %b %Y") + ")")
    print("Book:", book.get_title(), "by", book.get_author())
    member = ask("Issue to (member name): ", validate_member)
    library.issue_book(book.get_item_id(), member)
    print("Book issued to", book.get_issued_to() + ". Due date:", book.get_due_date().strftime("%d %b %Y"))


def return_book(library):
    book = library.get_book(input("Enter book ID to return: "))
    member = book.get_issued_to()
    book, overdue = library.return_book(book.get_item_id())
    print("'" + book.get_title() + "' returned by " + member + ".")
    if overdue:
        print("Note: the book was returned", overdue, "day(s) late.")
    else:
        print("Returned on time. Thank you!")


def display_available(library):
    books = library.available_books()
    if len(books) == 0:
        print("No books are available right now.")
        return
    print()
    print_table(books, show_status=False)
    print("\nAvailable: " + str(len(books)) + " of " + str(len(library.all_books())) + " books")


def save(library):
    if library.save_data():
        print("Records saved to books.csv.")


def main():
    library = Library()
    for msg in library.load_data():
        print(msg)

    while True:
        print(MENU)
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "7":
            save(library)
            print("Goodbye!")
            break

        try:
            if choice == "1":
                add_book(library)
            elif choice == "2":
                search_books(library)
            elif choice == "3":
                issue_book(library)
            elif choice == "4":
                return_book(library)
            elif choice == "5":
                display_available(library)
            elif choice == "6":
                save(library)
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")
        except (ValueError, Exception) as e:
            print("Error:", e)
        except KeyboardInterrupt:
            print("\nInput cancelled.")


if __name__ == "__main__":
    main()
