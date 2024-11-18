-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS weight;

-- Use the database
USE weight;

-- Create the table for containers
CREATE TABLE IF NOT EXISTS containers_registered (
    container_id VARCHAR(255) PRIMARY KEY,
    weight INT NOT NULL,
    unit VARCHAR(10) NOT NULL
);

-- Insert example data if the table is empty (Optional)
INSERT INTO containers_registered (container_id, weight, unit)
SELECT 'container1', 1000, 'kg'
UNION ALL
SELECT 'container2', 1500, 'kg'
UNION ALL
SELECT 'container3', 1200, 'kg';

-- Index for faster lookups by container_id (Optional but recommended)
CREATE INDEX idx_container_id ON containers_registered (container_id);

