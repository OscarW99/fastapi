-- We are using a relation database management system called PostgresSQL or just Postgres

-- a relational database is made of many tables that are linked
-- Need to specify data type in table column ([Int, decimal, precision], [Varchar, text], boolean, array)


-- A table must have a primary key to uniquely identify rows.

-- You can apply constraints to columns...
-- a UNIQUE constraint means all values in a column must be unique
-- the NOT NULL constraint means the column cannot be left blank (by default it can)

-- the serial datatype in postgres automatically gives each row an integer value.


-- Commands...
-- every sql command ends with a semi-colon


SELECT * from products;
-- basically just retrieves the whole 'products' table
-- * means all columns


SELECT name from products;
-- only retrieve name column from products table


SELECT name, id, price from products;
-- returns these threee columns. Note the order you write the columns will change the order you recieve them

-- capitalisation does NOT matter with SQL specific commands however it is best practice.

-- We can change the name of columns when we retrieve them...
SELECT id AS new_name FROM products;
-- ... you can do this for many columns at once....
SELECT id AS new_name, price as new_name_2 FROM products;

-- instead of getting all rows you can use the WHERE command to filter certain rows
SELECT * FROM products WHERE inventory = 2;
-- you must use single quotes for filtering strings
SELECT * FROM products WHERE name = 'TV';
SELECT * FROM products WHERE price < 40;
-- To say 'not' in SQL you use != or <>  ...
SELECT * FROM products WHERE inventory != 0;
SELECT * FROM products WHERE inventory <> 0;
-- The AND/OR commands allow multiple filters...
SELECT * FROM products WHERE inventory <> 0 AND price > 20;
SELECT * FROM products WHERE inventory <> 0 OR price > 20;

-- To select multiple items you can do...
SELECT * FROM products WHERE id = 1 OR id = 2 OR id = 3;
-- ...however this is long so we can use IN like with R...
SELECT * FROM products WHERE id IN (1,2,3);

--  Operators (same as python)
--  =
--  >
--  <
--  <=
--  >=

-- The LIKE operator allows for regex type filtering...
SELECT * FROM products WHERE name LIKE 'TV%'
-- this will get all products with a name that starts with 'TV'
-- You can add NOT in here and mover the %...
SELECT * FROM products WHERE name NOT LIKE '%e%'
-- this will get all products that don't have an 'e' in the name.

-- Ordering results
SELECT * FROM products ORDER BY price;
-- (ASC is deafault)
SELECT * FROM products ORDER BY price DESC;
-- Ordering on more than one plain... just add arguments seperated by a comma
SELECT * FROM products ORDER BY inventory DESC, price ASC;
-- to get the most recent item just dort by timestamp column

-- In reality the queries listed above will return potentially millions of rows depending on the size of our database. We need to set limits to how many rows are returned using the LIMIT command.
SELECT * FROM products where price > 20 ORDER BY created_at DESC LIMIT 3;
-- Just chain LIMIT X onto the end of a command.

-- OFFSET will skip past certain rows that meet the condition
SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2


-- -- Adding new entries into the database with INSERT INTO and a list of column names and a list of column values
INSERT INTO products (name, price, inventory) VALUES ('watch', 30, 20);
-- a 'INSERT 0 1' response means everything worked
-- The key word 'returning' will return at the end of an INSERT statement will return the new item back to the user. You must specify what columns you want returning (use * for all columns).
INSERT INTO products (name, price, inventory) VALUES ('sword', 63, 10) returning id, name;
-- To add many rows at the same time use the following format...
INSERT INTO products (name, price, inventory) VALUES ('x', y, z), ('x', y, z), ('x', y, z) returning *;

-- Deleting entries
DELETE FROM products WHERE id = 3;
-- retuens row before deleting it
DELETE FROM products WHERE id = 10 RETURNING *;


-- Updating existing data with UPDATE and SET commands
UPDATE products SET name = 'new_name', price = 333 WHERE id = 7;
UPDATE products SET name = 'ear-ring' WHERE id = 15 RETURNING *;
-- To update multiple rows ...
UPDATE products SET is_sale = true WHERE id > 15 RETURNING *;



-- We need a postgres driver to use a postgres databse within python. We use Psycopg for this. (sqla;chemy uses psycopg)


--! ## SQL JOINS ## (go to postgresqltutorial.com)
SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id;
--  This will jon tables posts and users. You can select columns from this join to return.. 
-- e.g.
SELECT title, content, email FROM posts LEFT JOIN users ON posts.user_id = users.id;
-- If 2 tables have the same column names you need to specify what columns you want to keep, e.g...
SELECT posts.id, email FROM posts LEFT JOIN users ON posts.user_id = users.id;
-- worth putting the table in front of variables anyway for clarity
SELECT posts.*, email FROM posts LEFT JOIN users ON posts.user_id = users.id;

--  A LEFT join will show you all things that exist in the left table and not necessarily the right, and the RIGHT join will do the opposite.

SELECT users.id, COUNT(*) FROM posts LEFT JOIN users ON posts.user_id = users.id group by users.id;
-- postgres has a builting COUNT() function to count a number of occurences. If you specify a column in COUNT() it will not count null values..
SELECT users.id, users.email, COUNT(posts.id) AS user_post_count FROM posts RIGHT JOIN users ON posts.user_id = users.id GROUP BY users.id;
-- The join we want to have in our get post(s) functions...
select posts.id, COUNT(votes.post_id) from posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;
