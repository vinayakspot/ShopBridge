create database shopbridgedb;

CREATE SEQUENCE item_sequence
  start 100
  increment 1;

 create table items(
    created_on TIMESTAMP DEFAULT NOW(),
    item_id integer PRIMARY KEY DEFAULT nextval('item_sequence'),
    item_name VARCHAR(50) NOT NULL,
    item_description TEXT NOT NULL,
    item_price NUMERIC NOT NULL
);

ALTER SEQUENCE item_sequence
OWNED BY items.item_id;
