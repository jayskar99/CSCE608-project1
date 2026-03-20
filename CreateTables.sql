CREATE TABLE PUBLISHER (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    address TEXT
);

CREATE TABLE BOOK (
    isbn VARCHAR(13) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    genre VARCHAR(100),
    publication_year INT,
    page_count INT,
    rating DECIMAL(3,2),
    publisher_id INT,
    FOREIGN KEY (publisher_id) REFERENCES PUBLISHER(id)
);

CREATE TABLE PERSON (
    card_number INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT
);

CREATE TABLE HISTORY (
    id INT PRIMARY KEY,
    checkout_dt DATETIME,
    due_date DATE,
    return_date DATE,
    isbn VARCHAR(13),
    card_number INT,
    FOREIGN KEY (isbn) REFERENCES BOOK(isbn),
    FOREIGN KEY (card_number) REFERENCES PERSON(card_number)
);

CREATE TABLE PRICE (
    id INT PRIMARY KEY,
    late_id INT,
    dollar_amount DECIMAL(10,2)
);

CREATE TABLE LATE (
    id INT PRIMARY KEY,
    history_id INT UNIQUE,
    amount_late INT,
    FOREIGN KEY (history_id) REFERENCES HISTORY(id)
);

CREATE TABLE FEE (
    id INT PRIMARY KEY,
    price_id INT,
    status VARCHAR(50),
    card_number INT,
    FOREIGN KEY (price_id) REFERENCES PRICE(id),
    FOREIGN KEY (card_number) REFERENCES PERSON(card_number)
);

CREATE TABLE RESERVATION (
    id INT PRIMARY KEY,
    end_date DATE,
    status VARCHAR(50),
    isbn VARCHAR(13),
    card_number INT,
    FOREIGN KEY (isbn) REFERENCES BOOK(isbn),
    FOREIGN KEY (card_number) REFERENCES PERSON(card_number)
);