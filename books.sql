CREATE TABLE books (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR2 (300) NOT NULL,
    price NUMBER (8, 2) NOT NULL,
    rating VARCHAR2 (10) NOT NULL,
    availability VARCHAR2 (50)
);

SELECT title, price, rating, availability
FROM books WHERE UPPER(title) LIKE UPPER('%termo%')
ORDER BY title;