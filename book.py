from main import getconnection
from colorama import Fore, Style

def addbook():
    db = getconnection()
    cursor = db.cursor()

    print(Fore.BLUE + 'You are adding a book')

    # Raw input for actual DB insert
    title = input(Fore.BLUE + "Enter the book name or title: ").strip()
    author = input(Fore.BLUE + "Enter the book author (if more than one authors, separate by commas): ").strip()
    genre = input(Fore.BLUE + "Enter the genre of book: ").strip()
    publisher = input(Fore.BLUE + "Enter the publisher: ").strip()
    quantity = int(input(Fore.BLUE + "Enter the quantity: "))
    year = input(Fore.BLUE + "Enter the year of publication of book: ").strip()

    # Normalized input for matching
    title_norm = title.strip().lower()
    author_norm = author.strip().lower()

    # DEBUG: See what will be checked
    #print(Fore.YELLOW + f"DEBUG: Checking for book where title='{title_norm}' and author='{author_norm}'")

    # SQL to check if book already exists
    check_query = """
        SELECT * FROM books
        WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s
    """
    cursor.execute(check_query, (title_norm, author_norm))
    existing_book = cursor.fetchone()

    # DEBUG: Show result from DB
    print(Fore.YELLOW + f"DEBUG: DB match result = {existing_book}")

    if existing_book:
        # Update quantity
        update_query = """
            UPDATE books
            SET quantity = %s
            WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s
        """
        cursor.execute(update_query, (quantity, title_norm, author_norm))
        db.commit()
        print(Fore.GREEN + "Book quantity updated successfully!")
    else:
        # Insert new book
        insert_query = """
            INSERT INTO books (title, author, genre, quantity, publisher, year_of_publication)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (title, author, genre, quantity, publisher, year))
        db.commit()
        print(Fore.GREEN + "Book added successfully!")

    cursor.close()
    db.close()
addbook()
