# book.py
# LibraryItem (abstract base class) and Book (inherits from LibraryItem).
# Kept in one file since LibraryItem only exists to support Book here.

from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

LOAN_DAYS = 14
DATE_FORMAT = "%Y-%m-%d"


# ---------------- validation helpers ----------------
def validate_title(value):
    value = " ".join(str(value).split())
    if value == "":
        raise ValueError("Title cannot be empty")
    if len(value) > 100:
        raise ValueError("Title is too long (maximum 100 characters)")
    return value


def validate_author(value):
    value = " ".join(str(value).split())
    if value == "":
        raise ValueError("Author cannot be empty")
    for ch in value:
        if not (ch.isalpha() or ch in " .'-&,"):
            raise ValueError("Author can only contain letters, spaces and . ' - & ,")
    return value


def validate_genre(value):
    value = " ".join(str(value).split())
    if value == "":
        raise ValueError("Genre cannot be empty")
    return value


def validate_year(value):
    try:
        year = int(str(value).strip())
    except ValueError:
        raise ValueError("Year must be a whole number")
    current = date.today().year
    if year < 1000 or year > current:
        raise ValueError("Year must be between 1000 and " + str(current))
    return year


def validate_member(value):
    value = " ".join(str(value).split())
    if value == "":
        raise ValueError("Member name cannot be empty")
    for ch in value:
        if not (ch.isalpha() or ch in " .'-"):
            raise ValueError("Name should only contain letters, spaces, dots, hyphens and apostrophes")
    return value


def parse_date(text):
    try:
        return datetime.strptime(str(text).strip(), DATE_FORMAT).date()
    except ValueError:
        raise ValueError("Invalid date '" + str(text) + "' (expected YYYY-MM-DD)")


# ---------------- LibraryItem (abstract) ----------------
class LibraryItem(ABC):
    def __init__(self, item_id, title):
        item_id = str(item_id).strip().upper()
        if item_id == "":
            raise ValueError("Book ID cannot be empty")
        self.__item_id = item_id      # id never changes
        self.__title = ""
        self.set_title(title)

    # ---- getters / setters ----
    def get_item_id(self):
        return self.__item_id

    def get_title(self):
        return self.__title

    def set_title(self, value):
        self.__title = validate_title(value)

    @abstractmethod
    def get_details(self):
        pass


class Book(LibraryItem):
    def __init__(self, book_id, title, author, genre, year,
                 issued_to="", issue_date="", due_date=""):
        super().__init__(book_id, title)
        self.__author = validate_author(author)
        self.__genre = validate_genre(genre)
        self.__year = validate_year(year)
        self.__issued_to = None
        self.__issue_date = None
        self.__due_date = None

        issued_to = str(issued_to or "").strip()
        if issued_to != "":
            self.__issued_to = validate_member(issued_to)
            self.__issue_date = parse_date(issue_date)
            self.__due_date = parse_date(due_date)
        elif str(issue_date or "").strip() != "" or str(due_date or "").strip() != "":
            raise ValueError("Dates given for a book that is not issued")

    # ---- getters / setters ----
    def get_author(self):
        return self.__author

    def set_author(self, value):
        self.__author = validate_author(value)

    def get_genre(self):
        return self.__genre

    def set_genre(self, value):
        self.__genre = validate_genre(value)

    def get_year(self):
        return self.__year

    def set_year(self, value):
        self.__year = validate_year(value)

    def get_issued_to(self):
        return self.__issued_to

    def get_issue_date(self):
        return self.__issue_date

    def get_due_date(self):
        return self.__due_date

    def is_available(self):
        return self.__issued_to is None

    # ---- issue / return ----
    def issue(self, member, issue_date=None):
        if not self.is_available():
            raise Exception("'" + self.get_title() + "' is already issued to " + self.__issued_to +
                            " (due " + self.__due_date.strftime("%d %b %Y") + ")")
        member = validate_member(member)
        if issue_date is None:
            issue_date = date.today()
        self.__issued_to = member
        self.__issue_date = issue_date
        self.__due_date = issue_date + timedelta(days=LOAN_DAYS)
        return self.__due_date

    def days_overdue(self, today=None):
        if self.is_available():
            return 0
        if today is None:
            today = date.today()
        days = (today - self.__due_date).days
        if days < 0:
            days = 0
        return days

    def return_book(self, return_date=None):
        if self.is_available():
            raise Exception("'" + self.get_title() + "' is not currently issued")
        overdue = self.days_overdue(return_date)
        self.__issued_to = None
        self.__issue_date = None
        self.__due_date = None
        return overdue

    # ---- display ----
    def status_text(self):
        if self.is_available():
            return "Available"
        if self.days_overdue() > 0:
            return "Overdue since " + self.__due_date.strftime("%d %b")
        return "Issued, due " + self.__due_date.strftime("%d %b")

    def get_details(self):
        return (self.get_item_id() + " | " + self.get_title() + " | " + self.__author +
                " | " + self.__genre + " | " + str(self.__year) + " | " + self.status_text())

    def __str__(self):
        return self.get_details()

    # ---- csv helpers ----
    def to_row(self):
        row = [self.get_item_id(), self.get_title(), self.__author, self.__genre, self.__year,
               "Available" if self.is_available() else "Issued",
               self.__issued_to if self.__issued_to else ""]
        row.append(self.__issue_date.strftime(DATE_FORMAT) if self.__issue_date else "")
        row.append(self.__due_date.strftime(DATE_FORMAT) if self.__due_date else "")
        return row


def book_from_row(row):
    status = (row.get("status") or "").strip().lower()
    issued_to = (row.get("issued_to") or "").strip()
    if status not in ("available", "issued"):
        raise ValueError("Unknown status '" + str(row.get("status")) + "'")
    if (status == "issued") != (issued_to != ""):
        raise ValueError("Status does not match the issued_to column")
    return Book(row.get("book_id") or "", row.get("title") or "",
               row.get("author") or "", row.get("genre") or "",
               row.get("year") or "", issued_to,
               row.get("issue_date") or "", row.get("due_date") or "")
