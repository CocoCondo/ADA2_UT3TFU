CREATE DATABASE recipes_db;
\c recipes_db;

CREATE TABLE recipes (
  id SERIAL PRIMARY KEY, 
  name TEXT NOT NULL, 
  steps TEXT);

CREATE TABLE recipe_items (
  recipe_id INT NOT NULL,
  product_id INT NOT NULL,
  qty NUMERIC NOT NULL,
  PRIMARY KEY (recipe_id, product_id)
);