-- ════════════════════════════════════════════════════════
-- Clean existing data (order matters due to foreign keys)
-- ════════════════════════════════════════════════════════
DELETE
FROM games;
DELETE
FROM publishers;
DELETE
FROM studios;

-- ════════════════════════════════════════════════════════
-- Insert studios (ID auto‑generated)
-- ════════════════════════════════════════════════════════
INSERT INTO studios (name, country, description)
VALUES ('Naughty Dog', 'USA', 'American studio known for The Last of Us and Uncharted.'),
       ('Rockstar North', 'UK', 'Scottish studio behind the Grand Theft Auto series.'),
       ('FromSoftware', 'Japan', 'Japanese studio famous for the Souls series and Elden Ring.'),
       ('CD Projekt Red', 'Poland', 'Polish studio behind The Witcher and Cyberpunk 2077.'),
       ('Nintendo EPD', 'Japan', 'Nintendo internal studio behind Zelda and Mario.'),
       ('Mojang', 'Sweden', 'Swedish studio that created Minecraft.'),
       ('Valve', 'USA', 'American studio behind Half-Life and Portal.'),
       ('Santa Monica Studio', 'USA', 'American studio behind the God of War series.'),
       ('Game Freak', 'Japan', 'Japanese studio developing the Pokémon games.'),
       ('Insomniac Games', 'USA', 'American studio behind Marvel''s Spider-Man and Ratchet & Clank.'),
       ('Ubisoft Montreal', 'Canada', 'Canadian studio behind Assassin''s Creed.'),
       ('Square Enix', 'Japan', 'Japanese studio behind the Final Fantasy series.');

-- ════════════════════════════════════════════════════════
-- Insert publishers (ID auto‑generated)
-- ════════════════════════════════════════════════════════
INSERT INTO publishers (name, country)
VALUES ('Sony Interactive Entertainment', 'Japan'),
       ('Nintendo', 'Japan'),
       ('Bandai Namco', 'Japan'),
       ('CD Projekt', 'Poland'),
       ('Take-Two Interactive', 'USA'),
       ('Microsoft', 'USA'),
       ('Valve', 'USA'),
       ('Ubisoft', 'France'),
       ('Square Enix', 'Japan'),
       ('Activision', 'USA');

-- ════════════════════════════════════════════════════════
-- Insert games – foreign keys resolved by name lookup
-- ════════════════════════════════════════════════════════
INSERT INTO games (code, title, studio_id, publisher_id, genre)
VALUES ('TLOU-001', 'The Last of Us',
        (SELECT id FROM studios WHERE name = 'Naughty Dog'),
        (SELECT id FROM publishers WHERE name = 'Sony Interactive Entertainment'),
        'Action'),

       ('TLOU2-001', 'The Last of Us Part II',
        (SELECT id FROM studios WHERE name = 'Naughty Dog'),
        (SELECT id FROM publishers WHERE name = 'Sony Interactive Entertainment'),
        'Action'),

       ('UNCH4-001', 'Uncharted 4: A Thief''s End',
        (SELECT id FROM studios WHERE name = 'Naughty Dog'),
        (SELECT id FROM publishers WHERE name = 'Sony Interactive Entertainment'),
        'Adventure'),

       ('GTAV-001', 'Grand Theft Auto V',
        (SELECT id FROM studios WHERE name = 'Rockstar North'),
        (SELECT id FROM publishers WHERE name = 'Take-Two Interactive'),
        'Action'),

       ('ER-001', 'Elden Ring',
        (SELECT id FROM studios WHERE name = 'FromSoftware'),
        (SELECT id FROM publishers WHERE name = 'Bandai Namco'),
        'RPG'),

       ('DS3-001', 'Dark Souls III',
        (SELECT id FROM studios WHERE name = 'FromSoftware'),
        (SELECT id FROM publishers WHERE name = 'Bandai Namco'),
        'RPG'),

       ('W3-001', 'The Witcher 3: Wild Hunt',
        (SELECT id FROM studios WHERE name = 'CD Projekt Red'),
        (SELECT id FROM publishers WHERE name = 'CD Projekt'),
        'RPG'),

       ('CP77-001', 'Cyberpunk 2077',
        (SELECT id FROM studios WHERE name = 'CD Projekt Red'),
        (SELECT id FROM publishers WHERE name = 'CD Projekt'),
        'RPG'),

       ('BOTW-001', 'The Legend of Zelda: Breath of the Wild',
        (SELECT id FROM studios WHERE name = 'Nintendo EPD'),
        (SELECT id FROM publishers WHERE name = 'Nintendo'),
        'Adventure'),

       ('MK8-001', 'Mario Kart 8 Deluxe',
        (SELECT id FROM studios WHERE name = 'Nintendo EPD'),
        (SELECT id FROM publishers WHERE name = 'Nintendo'),
        'Racing'),

       ('MC-001', 'Minecraft',
        (SELECT id FROM studios WHERE name = 'Mojang'),
        (SELECT id FROM publishers WHERE name = 'Microsoft'),
        'Simulation'),

       ('HL2-001', 'Half-Life 2',
        (SELECT id FROM studios WHERE name = 'Valve'),
        (SELECT id FROM publishers WHERE name = 'Valve'),
        'Shooter'),

       ('GOW-001', 'God of War',
        (SELECT id FROM studios WHERE name = 'Santa Monica Studio'),
        (SELECT id FROM publishers WHERE name = 'Sony Interactive Entertainment'),
        'Action'),

       ('POKE-001', 'Pokémon Scarlet',
        (SELECT id FROM studios WHERE name = 'Game Freak'),
        (SELECT id FROM publishers WHERE name = 'Nintendo'),
        'RPG'),

       ('SM-001', 'Marvel''s Spider-Man',
        (SELECT id FROM studios WHERE name = 'Insomniac Games'),
        (SELECT id FROM publishers WHERE name = 'Sony Interactive Entertainment'),
        'Action'),

       ('ACV-001', 'Assassin''s Creed Valhalla',
        (SELECT id FROM studios WHERE name = 'Ubisoft Montreal'),
        (SELECT id FROM publishers WHERE name = 'Ubisoft'),
        'Action'),

       ('FF7R-001', 'Final Fantasy VII Remake',
        (SELECT id FROM studios WHERE name = 'Square Enix'),
        (SELECT id FROM publishers WHERE name = 'Square Enix'),
        'RPG'),

-- FromSoftware gets a second publisher (Activision) to showcase the
-- "distinct publishers per studio" search.
       ('SEKIRO-001', 'Sekiro: Shadows Die Twice',
        (SELECT id FROM studios WHERE name = 'FromSoftware'),
        (SELECT id FROM publishers WHERE name = 'Activision'),
        'Action');
