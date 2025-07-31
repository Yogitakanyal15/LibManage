from main import getconnection
from colorama import Fore, Style

db = getconnection()
cursor = db.cursor()

def addbook():

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

    try:
        if existing_book:
            # Update quantity
            update_query = """
                UPDATE books
                SET quantity = quantity + %s
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
    except Exception as e:
        print(Fore.RED+"Error Occured: ",e)

    print(FORE.MAGENTA+"THANK YOU!")

    

def updatebook():
    book = input(Fore.BLUE + "Enter the book name or title: ").strip().lower()
    author = input(Fore.BLUE + "Enter the author: ").strip().lower()
    ch = 'y'

    while ch.lower() == 'y':
        print(Fore.BLUE + """\nWhat do you want to update?
1. Book Name
2. Author Name
3. Genre
4. Quantity
5. Publisher
6. Year of Publication""")

        ip = input(Fore.BLUE + "Enter your choice: ").strip()

        try:
            if ip == '1':
                new_value = input(Fore.BLUE + "Enter the new book name or title: ").strip()
                query = "UPDATE books SET title = %s WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s"
                values = (new_value, book, author)

            elif ip == '2':
                new_value = input(Fore.BLUE + "Enter the new author: ").strip()
                query = "UPDATE books SET author = %s WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s"
                values = (new_value, book, author)

            elif ip == '3':
                new_value = input(Fore.BLUE + "Enter the new genre: ").strip()
                query = "UPDATE books SET genre = %s WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s"
                values = (new_value, book, author)

            elif ip == '4':
                new_value = int(input(Fore.BLUE + "Enter the new quantity: ").strip())
                query = "UPDATE books SET quantity = %s WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s"
                values = (new_value, book, author)

            elif ip == '5':
                new_value = input(Fore.BLUE + "Enter the new publisher: ").strip()
                query = "UPDATE books SET publisher = %s WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s"
                values = (new_value, book, author)

            elif ip == '6':
                new_value = int(input(Fore.BLUE + "Enter the new year of publication: ").strip())
                query = "UPDATE books SET year_of_publication = %s WHERE LOWER(TRIM(title)) = %s AND LOWER(TRIM(author)) = %s"
                values = (new_value, book, author)

            else:
                print(Fore.RED + "Invalid Choice!")
                continue

            cursor.execute(query, values)
            db.commit()
            print(Fore.GREEN + "Updated successfully!")

        except Exception as e:
            print(Fore.RED + "Error occurred:", e)
            db.rollback()

        ch = input(Fore.BLUE + "Do you want to update more? (Type Y or y for yes): ").strip()

    print(Fore.MAGENTA + "THANK YOU!")

addbook()
cursor.close()
db.close()
