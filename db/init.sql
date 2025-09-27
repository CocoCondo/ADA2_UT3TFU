-- db/init.sql
CREATE TABLE products (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL, unit TEXT NOT NULL);
CREATE TABLE recipes (id SERIAL PRIMARY KEY, name TEXT NOT NULL, steps TEXT);
CREATE TABLE recipe_items (
  recipe_id INT REFERENCES recipes(id) ON DELETE CASCADE,
  product_id INT REFERENCES products(id) ON DELETE RESTRICT,
  qty NUMERIC NOT NULL,
  PRIMARY KEY (recipe_id, product_id)
);
CREATE TABLE shopping_lists (id SERIAL PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE shopping_list_items (
  list_id INT REFERENCES shopping_lists(id) ON DELETE CASCADE,
  product_id INT REFERENCES products(id),
  qty NUMERIC NOT NULL
);
