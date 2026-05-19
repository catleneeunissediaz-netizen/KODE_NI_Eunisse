-- ================================================================
--  ALING PURING'S MULTI-BRANCH SARI-SARI STORE MANAGEMENT SYSTEM
--  MySQL Database Setup Script
--  Run this in phpMyAdmin (XAMPP) before starting the Python app
-- ================================================================

-- Step 1: Create and select the database
CREATE DATABASE IF NOT EXISTS aling_puring
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE aling_puring;

-- ================================================================
--  TABLE: branches
--  Stores each store branch (name + location)
-- ================================================================
CREATE TABLE IF NOT EXISTS branches (
    branch_id   VARCHAR(60)   PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    location    VARCHAR(150)  NOT NULL,
    created_at  DATETIME      DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================
--  TABLE: inventory
--  Each branch has its own separate inventory rows
-- ================================================================
CREATE TABLE IF NOT EXISTS inventory (
    id              INT           AUTO_INCREMENT PRIMARY KEY,
    branch_id       VARCHAR(60)   NOT NULL,
    name            VARCHAR(100)  NOT NULL,
    price           DECIMAL(10,2) NOT NULL,
    stock           INT           NOT NULL DEFAULT 0,
    restock_level   INT           NOT NULL DEFAULT 5,
    updated_at      DATETIME      DEFAULT CURRENT_TIMESTAMP
                                  ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_branch_product (branch_id, name),
    FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id) ON DELETE CASCADE
);

-- ================================================================
--  TABLE: transactions
--  One row per customer sale visit
-- ================================================================
CREATE TABLE IF NOT EXISTS transactions (
    txn_id        INT           AUTO_INCREMENT PRIMARY KEY,
    branch_id     VARCHAR(60)   NOT NULL,
    branch_name   VARCHAR(100)  NOT NULL,
    total_amount  DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id) ON DELETE CASCADE
);

-- ================================================================
--  TABLE: transaction_items
--  Line items for each transaction
-- ================================================================
CREATE TABLE IF NOT EXISTS transaction_items (
    item_id   INT           AUTO_INCREMENT PRIMARY KEY,
    txn_id    INT           NOT NULL,
    name      VARCHAR(100)  NOT NULL,
    qty       INT           NOT NULL,
    price     DECIMAL(10,2) NOT NULL,
    subtotal  DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (txn_id)
        REFERENCES transactions(txn_id) ON DELETE CASCADE
);

-- ================================================================
--  SAMPLE DATA  (3 branches + products -- safe to delete if unneeded)
-- ================================================================

INSERT IGNORE INTO branches (branch_id, name, location) VALUES
    ('main_branch',   'Main Branch',   'Barangay Batasan Hills'),
    ('second_branch', 'Second Branch', 'Barangay Holy Spirit'),
    ('third_branch',  'Third Branch',  'Barangay Payatas');

-- Main Branch products
INSERT IGNORE INTO inventory (branch_id, name, price, stock, restock_level) VALUES
    ('main_branch', 'Chippy',            10.00, 50, 10),
    ('main_branch', 'Nova',              10.00, 45, 10),
    ('main_branch', 'Royal Tru-Orange',  15.00, 30,  5),
    ('main_branch', 'Coke Mismo',        15.00, 40,  5),
    ('main_branch', 'Lucky Me Noodles',  12.00, 60, 15),
    ('main_branch', 'Tide Sachet',        8.00, 35, 10),
    ('main_branch', 'Bear Brand Sachet', 14.00, 25,  5),
    ('main_branch', 'Silver Swan Soy',   22.00, 20,  5);

-- Second Branch products
INSERT IGNORE INTO inventory (branch_id, name, price, stock, restock_level) VALUES
    ('second_branch', 'Chippy',            10.00, 30, 10),
    ('second_branch', 'Piattos',           15.00, 25,  5),
    ('second_branch', 'Coke Mismo',        15.00, 50,  5),
    ('second_branch', 'C2 Apple',          18.00, 40,  8),
    ('second_branch', 'Lucky Me Noodles',  12.00, 55, 15),
    ('second_branch', 'Safeguard Soap',    20.00, 18,  5);

-- Third Branch products
INSERT IGNORE INTO inventory (branch_id, name, price, stock, restock_level) VALUES
    ('third_branch', 'Boy Bawang',        10.00, 40, 10),
    ('third_branch', 'Coke Mismo',        15.00, 35,  5),
    ('third_branch', 'Sprite Mismo',      15.00, 35,  5),
    ('third_branch', 'Lucky Me Noodles',  12.00, 70, 15),
    ('third_branch', 'Milo Sachet',       14.00, 30,  8),
    ('third_branch', 'Ariel Sachet',       9.00, 22,  5);

-- ================================================================
--  VERIFY
-- ================================================================
SHOW TABLES;
SELECT 'Setup complete! Database is ready.' AS Status;
