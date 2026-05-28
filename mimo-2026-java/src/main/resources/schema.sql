DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS studios;
DROP TABLE IF EXISTS publishers;

-- Create studios table (game development studios)
CREATE TABLE IF NOT EXISTS studios (
   id BIGINT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100),
    description VARCHAR(500)
    );

-- Create publishers table
CREATE TABLE IF NOT EXISTS publishers (
     id BIGINT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100)
    );

CREATE TABLE IF NOT EXISTS games(
       code VARCHAR(20) PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       studio_id BIGINT NOT NULL,
       publisher_id BIGINT NOT NULL,
       genre VARCHAR(50) NOT NULL,
       FOREIGN KEY (studio_id) REFERENCES studios(id) ON DELETE cascade,
       FOREIGN KEY (publisher_id) REFERENCES publishers(id)
);
