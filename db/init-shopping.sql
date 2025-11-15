CREATE DATABASE shopping_db;
\c shopping_db;
CREATE TABLE shopping_lists (
  id SERIAL PRIMARY KEY, 
  name TEXT NOT NULL);

CREATE TABLE shopping_list_items (
  list_id INT NOT NULL,
  product_id INT NOT NULL,
  qty NUMERIC NOT NULL,
  PRIMARY KEY (list_id, product_id)
);

