CREATE DATABASE products_db;
\c products_db;

CREATE TABLE products (
  id SERIAL PRIMARY KEY, 
  name TEXT UNIQUE NOT NULL, 
  unit TEXT NOT NULL);