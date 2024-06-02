import mysql.connector
from mysql.connector import Error

# Database connection
def create_connection():
    """Create a database connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='library_management',
            user='your_username',
            password='your_password'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Data Definition Language (DDL)
def create_tables():
    """Create necessary tables in the library_management database."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author_id INT,
                genre_id INT,
                isbn VARCHAR(13) NOT NULL,
                publication_date DATE,
                availability BOOLEAN DEFAULT 1,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (genre_id) REFERENCES genres(id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                biography TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS genres (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(50)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                library_id VARCHAR(10) NOT NULL UNIQUE
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrowed_books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                book_id INT,
                borrow_date DATE NOT NULL,
                return_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            );
        """)
        connection.commit()
        cursor.close()
        connection.close()
        print("Tables created successfully.")

# Adding a new book
def add_book(title, author_id, genre_id, isbn, publication_date):
    """Add a new book to the books table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO books (title, author_id, genre_id, isbn, publication_date)
                VALUES (%s, %s, %s, %s, %s);
            """, (title, author_id, genre_id, isbn, publication_date))
            connection.commit()
            print("Book added successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Borrow a book
def borrow_book(user_id, book_id, borrow_date):
    """Borrow a book by updating the availability and adding a record to borrowed_books."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE books SET availability = 0 WHERE id = %s AND availability = 1;", (book_id,))
            if cursor.rowcount == 0:
                print("Book is already borrowed or does not exist.")
                return
            cursor.execute("""
                INSERT INTO borrowed_books (user_id, book_id, borrow_date)
                VALUES (%s, %s, %s);
            """, (user_id, book_id, borrow_date))
            connection.commit()
            print("Book borrowed successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Return a book
def return_book(book_id, return_date):
    """Return a book by updating the availability and the return_date in borrowed_books."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE books SET availability = 1 WHERE id = %s;", (book_id,))
            cursor.execute("UPDATE borrowed_books SET return_date = %s WHERE book_id = %s AND return_date IS NULL;", (return_date, book_id))
            connection.commit()
            print("Book returned successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Search for a book
def search_book_by_isbn(isbn):
    """Search for a book by ISBN."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books WHERE isbn = %s;", (isbn,))
            row = cursor.fetchone()
            if row:
                print(f"Book found: {row}")
            else:
                print("No book found with the given ISBN.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Display all books
def display_all_books():
    """Display all books in the books table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Add a new user
def add_user(name, library_id):
    """Add a new user to the users table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (name, library_id)
                VALUES (%s, %s);
            """, (name, library_id))
            connection.commit()
            print("User added successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# View user details
def view_user_details(library_id):
    """View details of a user by their library_id."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE library_id = %s;", (library_id,))
            row = cursor.fetchone()
            if row:
                print(f"User details: {row}")
            else:
                print("No user found with the given library ID.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Display all users
def display_all_users():
    """Display all users in the users table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Main menu
def main_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\nWelcome to the Library Management System with Database Integration!")
        print("**** Main Menu ****")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Genre Operations")
        print("5. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            book_operations()
        elif choice == '2':
            user_operations()
        elif choice == '3':
            author_operations()
        elif choice == '4':
            genre_operations()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Book operations menu
def book_operations():
    """Display the book operations menu and handle user input."""
    while True:
        print("\n**** Book Operations ****")
        print("1. Add a new book")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            title = input("Enter book title: ")
            author_id = int(input("Enter author ID: "))
            genre_id = int(input("Enter genre ID: "))
            isbn = input("Enter ISBN: ")
            publication_date = input("Enter publication date (YYYY-MM-DD): ")
            add_book(title, author_id, genre_id, isbn, publication_date)
        elif choice == '2':
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            borrow_date = input("Enter borrow date (YYYY-MM-DD): ")
            borrow_book(user_id, book_id, borrow_date)
        elif choice == '3':
            book_id = int(input("Enter book ID: "))
            return_date = input("Enter return date (YYYY-MM-DD): ")
            return_book(book_id, return_date)
        elif choice == '4':
            isbn = input("Enter ISBN: ")
            search_book_by_isbn(isbn)
        elif choice == '5':
            display_all_books()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

# User operations menu
def user_operations():
    """Display the user operations menu and handle user input."""
    while True:
        print("\n**** User Operations ****")
        print("1. Add a new user")
        print("2. View user details")
        print("3. Display all users")
        print("4. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter user name: ")
            library_id = input("Enter library ID: ")
            add_user(name, library_id)
        elif choice == '2':
            library_id = input("Enter library ID: ")
            view_user_details(library_id)
        elif choice == '3':
            display_all_users()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Author operations menu
def author_operations():
    """Display the author operations menu and handle user input."""
    while True:
        print("\n**** Author Operations ****")
        print("1. Add a new author")
        print("2. View author details")
        print("3. Display all authors")
        print("4. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter author name: ")
            biography = input("Enter author biography: ")
            add_author(name, biography)
        elif choice == '2':
            author_id = int(input("Enter author ID: "))
            view_author_details(author_id)
        elif choice == '3':
            display_all_authors()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Add a new author
def add_author(name, biography):
    """Add a new author to the authors table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO authors (name, biography)
                VALUES (%s, %s);
            """, (name, biography))
            connection.commit()
            print("Author added successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# View author details
def view_author_details(author_id):
    """View details of an author by their ID."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM authors WHERE id = %s;", (author_id,))
            row = cursor.fetchone()
            if row:
                print(f"Author details: {row}")
            else:
                print("No author found with the given ID.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Display all authors
def display_all_authors():
    """Display all authors in the authors table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM authors;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Genre operations menu
def genre_operations():
    """Display the genre operations menu and handle user input."""
    while True:
        print("\n**** Genre Operations ****")
        print("1. Add a new genre")
        print("2. View genre details")
        print("3. Display all genres")
        print("4. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter genre name: ")
            description = input("Enter genre description: ")
            category = input("Enter genre category: ")
            add_genre(name, description, category)
        elif choice == '2':
            genre_id = int(input("Enter genre ID: "))
            view_genre_details(genre_id)
        elif choice == '3':
            display_all_genres()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Add a new genre
def add_genre(name, description, category):
    """Add a new genre to the genres table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO genres (name, description, category)
                VALUES (%s, %s, %s);
            """, (name, description, category))
            connection.commit()
            print("Genre added successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# View genre details
def view_genre_details(genre_id):
    """View details of a genre by their ID."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM genres WHERE id = %s;", (genre_id,))
            row = cursor.fetchone()
            if row:
                print(f"Genre details: {row}")
            else:
                print("No genre found with the given ID.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Display all genres
def display_all_genres():
    """Display all genres in the genres table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM genres;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Entry point
if __name__ == '__main__':
    create_tables()
    main_menu()
