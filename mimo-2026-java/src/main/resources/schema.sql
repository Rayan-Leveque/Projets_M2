DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS publishers;

-- Create authors table
CREATE TABLE IF NOT EXISTS authors (
   id BIGINT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100),
    biography VARCHAR(500)
    );

-- Create publishers table
CREATE TABLE IF NOT EXISTS publishers (
     id BIGINT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100)
    );

CREATE TABLE IF NOT EXISTS books(
       isbn VARCHAR(17) PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       author_id BIGINT NOT NULL,
       publisher_id BIGINT NOT NULL,
       category VARCHAR(50) NOT NULL,
       FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE cascade,
       FOREIGN KEY (publisher_id) REFERENCES publishers(id)
);

