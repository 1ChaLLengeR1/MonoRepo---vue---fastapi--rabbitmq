CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SET client_encoding TO 'UTF8';

CREATE TABLE user_one (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255)
    age VARCHAR(255)
    city VARCHAR(255)
);




