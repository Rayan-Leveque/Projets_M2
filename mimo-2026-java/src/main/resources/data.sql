-- ════════════════════════════════════════════════════════
-- Clean existing data (order matters due to foreign keys)
-- ════════════════════════════════════════════════════════
DELETE
FROM books;
DELETE
FROM publishers;
DELETE
FROM authors;

-- ════════════════════════════════════════════════════════
-- Insert authors (ID auto‑generated)
-- ════════════════════════════════════════════════════════
INSERT INTO authors (name, country, biography)
VALUES ('J.K. Rowling', 'UK', 'British author, best known for the Harry Potter series.'),
       ('Laure Moulin', 'France', 'Biographer and sister of Jean Moulin.'),
       ('Antoine de Saint-Exupéry', 'France', 'French writer and aviator, author of The Little Prince.'),
       ('George Orwell', 'UK', 'English novelist and essayist, famous for 1984 and Animal Farm.'),
       ('Yuval Noah Harari', 'Israel', 'Israeli historian and author of Sapiens.'),
       ('Albert Camus', 'France', 'French philosopher and author, Nobel Prize winner.'),
       ('Frank Herbert', 'USA', 'American science fiction writer, creator of Dune.'),
       ('Arthur Conan Doyle', 'UK', 'Scottish writer, creator of Sherlock Holmes.'),
       ('James Clear', 'USA', 'American author and speaker on habits and decision making.'),
       ('J.R.R. Tolkien', 'UK', 'English writer and philologist, author of The Lord of the Rings.'),
       ('Marjane Satrapi', 'Iran', 'Iranian-born French graphic novelist, author of Persepolis.'),
       ('Stephen Hawking', 'UK', 'English theoretical physicist and cosmologist.');

-- ════════════════════════════════════════════════════════
-- Insert publishers (ID auto‑generated)
-- ════════════════════════════════════════════════════════
INSERT INTO publishers (name, country)
VALUES ('Gallimard', 'France'),
       ('Livre de Poche', 'France'),
       ('Penguin', 'USA'),
       ('Flammarion', 'France'),
       ('HarperCollins', 'USA'),
       ('Robert Laffont', 'France'),
       ('Hachette', 'France'),
       ('Random House', 'USA'),
       ('Del Rey', 'USA'),
       ('L''Iconoclaste', 'France');

-- ════════════════════════════════════════════════════════
-- Insert books – foreign keys resolved by name lookup
-- ════════════════════════════════════════════════════════
INSERT INTO books (isbn, title, author_id, publisher_id, category)
VALUES ('9782070429158', 'Harry Potter à l''école des sorciers',
        (SELECT id FROM authors WHERE name = 'J.K. Rowling'),
        (SELECT id FROM publishers WHERE name = 'Flammarion'),
        'Fiction'),

       ('9782253151241', 'Jean Moulin : Biographie',
        (SELECT id FROM authors WHERE name = 'Laure Moulin'),
        (SELECT id FROM publishers WHERE name = 'Livre de Poche'),
        'Biography'),

       ('9782070612758', 'Le Petit Prince',
        (SELECT id FROM authors WHERE name = 'Antoine de Saint-Exupéry'),
        (SELECT id FROM publishers WHERE name = 'Gallimard'),
        'Fiction'),

       ('9780451524935', '1984',
        (SELECT id FROM authors WHERE name = 'George Orwell'),
        (SELECT id FROM publishers WHERE name = 'Penguin'),
        'Fiction'),

       ('9782226257017', 'Sapiens : Une brève histoire de l''humanité',
        (SELECT id FROM authors WHERE name = 'Yuval Noah Harari'),
        (SELECT id FROM publishers WHERE name = 'Hachette'),
        'History'),

       ('9782070360024', 'L''Étranger',
        (SELECT id FROM authors WHERE name = 'Albert Camus'),
        (SELECT id FROM publishers WHERE name = 'Flammarion'),
        'NonFiction'),

       ('9782221002247', 'Dune',
        (SELECT id FROM authors WHERE name = 'Frank Herbert'),
        (SELECT id FROM publishers WHERE name = 'Robert Laffont'),
        'SciFi'),

       ('9782253006329', 'Une étude en rouge',
        (SELECT id FROM authors WHERE name = 'Arthur Conan Doyle'),
        (SELECT id FROM publishers WHERE name = 'Livre de Poche'),
        'Fiction'),

       ('9780857197689', 'Atomic Habits',
        (SELECT id FROM authors WHERE name = 'James Clear'),
        (SELECT id FROM publishers WHERE name = 'Random House'),
        'NonFiction'),

       ('9782266154116', 'Le Seigneur des Anneaux',
        (SELECT id FROM authors WHERE name = 'J.R.R. Tolkien'),
        (SELECT id FROM publishers WHERE name = 'Del Rey'),
        'Fiction'),

       ('9782844140586', 'Persépolis',
        (SELECT id FROM authors WHERE name = 'Marjane Satrapi'),
        (SELECT id FROM publishers WHERE name = 'L''Iconoclaste'),
        'Fiction'),

       ('9782081238626', 'Une brève histoire du temps',
        (SELECT id FROM authors WHERE name = 'Stephen Hawking'),
        (SELECT id FROM publishers WHERE name = 'Flammarion'),
        'Science');

-- Additional books to create multiple publishers per author
INSERT INTO books (isbn, title, author_id, publisher_id, category) VALUES
       -- J.K. Rowling gets a second publisher (Gallimard)
       ('9782070643035', 'Harry Potter et la Chambre des secrets',
        (SELECT id FROM authors WHERE name = 'J.K. Rowling'),
        (SELECT id FROM publishers WHERE name = 'Gallimard'),
        'Fiction'),

       -- Stephen Hawking gets Penguin as second publisher
       ('9780553804362', 'The Universe in a Nutshell',
        (SELECT id FROM authors WHERE name = 'Stephen Hawking'),
        (SELECT id FROM publishers WHERE name = 'Penguin'),
        'Science'),

       -- George Orwell gets HarperCollins (new publisher)
       ('9780156262248', 'Homage to Catalonia',
        (SELECT id FROM authors WHERE name = 'George Orwell'),
        (SELECT id FROM publishers WHERE name = 'HarperCollins'),
        'NonFiction'),

       -- J.R.R. Tolkien gets HarperCollins (second publisher)
       ('9780261102217', 'The Hobbit',
        (SELECT id FROM authors WHERE name = 'J.R.R. Tolkien'),
        (SELECT id FROM publishers WHERE name = 'HarperCollins'),
        'Fiction');