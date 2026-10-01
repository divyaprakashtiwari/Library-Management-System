# Library Management System (Mini Project 1)

A console-based Python application that manages a library's books using
Object-Oriented Programming. Records are stored in a CSV file.

## Features
1. Add books
2. Search books (by ID, title, author, genre or member name)
3. Issue books (14-day loan period)
4. Return books (tells you if the book was late)
5. Display available books
6. Save records

Tip: search for `available`, `issued` or `overdue` to list books by status.

## How to run
```
python main.py
```
Requires Python 3.8+ (no external libraries). Keep all files in the same folder.

## Project files
| File | Purpose |
|---|---|
| `book.py` | `LibraryItem` (abstract base class), `Book` (derived class), issue/return logic, validation functions |
| `library.py` | `Library` manager class (all features + CSV file handling) |
| `main.py` | Console menu |
| `books.csv` | Sample data (24 books, 7 currently issued) |

## Classes
- **LibraryItem (abstract base class)**: Uses the `abc` module. Holds a
  read-only private item ID and a private title accessed through
  `get_title()`/`set_title()`, and an abstract method `get_details()`.
- **Book (derived class)**: Inherits from `LibraryItem`. Adds private author,
  genre, year and loan details (member, issue date, due date). Provides
  `issue()`, `return_book()`, `days_overdue()`, `status_text()` and a
  `to_row()` helper for CSV.
- **Library**: Keeps all books in a dictionary. Adds, searches, issues and
  returns books, lists available books, and loads/saves `books.csv`.
- **Validation functions**: `validate_title`, `validate_author`,
  `validate_genre`, `validate_year`, `validate_member`, `parse_date` (in
  `book.py`) raise `ValueError` with a clear message when given bad input.

## Loan rules
- A book is issued for 14 days from the day it is issued.
- A book already issued cannot be issued again until it is returned.
- On return, the program reports how many days late it was (if any).
- Adding the same title by the same author twice is blocked.

## Sample data
`books.csv` has 24 well-known books (Indian authors, world classics,
programming and self-help titles). Seven are issued to members, and two of
those are overdue, so the late-return message can be demonstrated.
New books get the next free ID (B125, B126, ...).

Columns: `book_id, title, author, genre, year, status, issued_to, issue_date, due_date`

Note: the sample due dates are set around 20 September 2026. On a different
date, the overdue/due status shown will change accordingly.

## OOP concepts used
| Concept | Where |
|---|---|
| Classes & Objects | `LibraryItem`, `Book`, `Library` |
| Encapsulation | Private attributes with `get_x()`/`set_x()` methods in `LibraryItem`, `Book`, `Library` |
| Inheritance | `Book(LibraryItem)` |
| Abstraction | `LibraryItem(ABC)` with `@abstractmethod get_details()` |
| File Handling | Read/write `books.csv` using the `csv` module |
| Exception Handling | Invalid title/author/year/name, book not found, already issued, not issued, duplicates, missing file, corrupted CSV rows |

## Notes
- Invalid input is re-asked instead of crashing the program.
- Bad rows in the CSV are skipped with a message; the rest still load.
- If `books.csv` is missing, the program starts empty and creates it on save.
- Choose option 6 or 7 to save; changes are not saved automatically.
