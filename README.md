# Library Management System with Database Integration

## Project Description

This project integrates a MySQL database with Python to develop an advanced Library Management System. The system is command-line based and allows users to browse, borrow, return, and explore a collection of books. It also supports managing users, authors, and genres.

## Features

- **Book Operations**: Add, borrow, return, search, and display books.
- **User Operations**: Add, view details, and display users.
- **Author Operations**: Add, view details, and display authors.
- **Genre Operations**: Add, view details, and display genres.

## Database Schema

### Books Table
```sql
CREATE TABLE books (
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
