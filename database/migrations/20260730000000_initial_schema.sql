-- migrate:up

-- please implement the initial schema below.

CREATE TABLE customers(
    id integer primary key not null,
    name varchar not null,
    street varchar not null,
    postal_code varchar not null,
    municipality varchar not null
);

CREATE TABLE status(
    status varchar primary key not null
);

INSERT INTO status(status) VALUES ('open'), ('in progress'), ('done');

CREATE TABLE projects(
    id integer primary key not null,
    customer_id integer not null references customers(id),
    date date not null,
    task varchar not null,
    location varchar,
    description varchar,
    status varchar not null references status(status)
);

-- migrate:down

-- please implement rollback SQL below.
-- in case you don't know regrets, use `SELECT 1`
DROP TABLE projects;
DROP TABLE status;
DROP TABLE customers;