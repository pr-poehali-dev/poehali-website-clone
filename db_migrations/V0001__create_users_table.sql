
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    energy_balance INTEGER DEFAULT 100,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (email, password_hash, energy_balance, is_admin) 
VALUES ('suradaniil74@gmail.com', '$2b$10$XYZ123placeholder', 1000, TRUE);
