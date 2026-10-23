-- CREATE TABLE IF NOT EXISTS mainmenu (
--     id integer PRIMARY KEY AUTOINCREMENT,
--     title text NOT NULL,
--     url text NOT NULL
-- );

-- INSERT INTO mainmenu
--     VALUES (1, "Головна", "/"),
--             (2, "Добавить статтю", "add_post");



-- CREATE TABLE IF NOT EXISTS product_images (
--     image_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     product_id INTEGER NOT NULL,
--     name TEXT NOT NULL,
--     image BLOB NOT NULL
-- );

-- ALTER TABLE product_images ADD COLUMN arrival_date TEXT;

ALTER TABLE product_images RENAME COLUMN product_id TO model;


