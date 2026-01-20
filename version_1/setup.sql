-- ============================================================
-- COMPLETE DATABASE SETUP FOR AI DOCUMENT ASSISTANT
-- ============================================================

-- ============================================================
-- STEP 1: CREATE DATABASE AND SCHEMA
-- ============================================================

-- Create database (skip if you already have one)
CREATE DATABASE IF NOT EXISTS AIFAQ_VERSION1_DB;

-- Use the database
USE DATABASE AIFAQ_VERSION1_DB;

-- Create schema
CREATE SCHEMA IF NOT EXISTS APP_SCHEMA;

-- Use the schema
USE SCHEMA APP_SCHEMA;

-- ============================================================
-- STEP 2: CREATE WAREHOUSE (if you don't have one)
-- ============================================================

CREATE WAREHOUSE IF NOT EXISTS AIFAQ_WAREHOUSE
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = FALSE;

-- Use the warehouse
USE WAREHOUSE AIFAQ_WAREHOUSE;

-- ============================================================
-- STEP 3: CREATE TABLES
-- ============================================================

-- 1. DOCUMENTS TABLE - Stores metadata about uploaded documents
CREATE OR REPLACE TABLE DOCUMENTS (
    DOC_ID VARCHAR(255) NOT NULL PRIMARY KEY,
    FILENAME VARCHAR(500) NOT NULL,
    FILE_TYPE VARCHAR(50) NOT NULL,
    FILE_SIZE INTEGER NOT NULL,
    IS_PUBLIC BOOLEAN DEFAULT FALSE,
    UPLOADED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 2. CHUNKS TABLE - Stores document text chunks for RAG
CREATE OR REPLACE TABLE CHUNKS (
    CHUNK_ID VARCHAR(255) NOT NULL PRIMARY KEY,
    DOC_ID VARCHAR(255) NOT NULL,
    CHUNK_INDEX INTEGER NOT NULL,
    CHUNK_TEXT TEXT NOT NULL
);

-- 3. EMBEDDINGS TABLE - Stores vector embeddings for semantic search
CREATE OR REPLACE TABLE EMBEDDINGS (
    CHUNK_ID VARCHAR(255) NOT NULL PRIMARY KEY,
    EMBEDDING VECTOR(FLOAT, 768) NOT NULL
);

-- 4. CHAT_HISTORY TABLE - Stores conversation history
CREATE OR REPLACE TABLE CHAT_HISTORY (
    CHAT_ID VARCHAR(255) NOT NULL PRIMARY KEY,
    SESSION_ID VARCHAR(255) NOT NULL,
    QUERY_TEXT TEXT NOT NULL,
    RESPONSE_TEXT TEXT,
    QUERY_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================
-- STEP 4: GRANT PERMISSIONS (Adjust role as needed)
-- ============================================================

-- Grant usage on database and schema
GRANT USAGE ON DATABASE AIFAQ_VERSION1_DB TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA AIFAQ_VERSION1_DB.APP_SCHEMA TO ROLE PUBLIC;

-- Grant permissions on tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA AIFAQ_VERSION1_DB.APP_SCHEMA TO ROLE PUBLIC;

-- Grant permissions for future tables
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA AIFAQ_VERSION1_DB.APP_SCHEMA TO ROLE PUBLIC;

-- Grant warehouse usage
GRANT USAGE ON WAREHOUSE AIFAQ_WAREHOUSE TO ROLE PUBLIC;

-- ============================================================
-- STEP 5: VERIFY CORTEX FUNCTIONS ARE AVAILABLE
-- ============================================================

-- Test embedding function (should return a vector)
SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', 'Test text for embedding') AS test_embedding;

-- Test LLM completion function
SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-7b', 'Say hello in one word') AS test_completion;

-- ============================================================
-- STEP 6: VERIFY SETUP
-- ============================================================

-- Show all tables
SHOW TABLES IN SCHEMA AIFAQ_VERSION1_DB.APP_SCHEMA;

-- Describe each table
DESCRIBE TABLE DOCUMENTS;
DESCRIBE TABLE CHUNKS;
DESCRIBE TABLE EMBEDDINGS;
DESCRIBE TABLE CHAT_HISTORY;

-- Show current context
SELECT 
    CURRENT_DATABASE() AS current_database,
    CURRENT_SCHEMA() AS current_schema,
    CURRENT_WAREHOUSE() AS current_warehouse,
    CURRENT_ROLE() AS current_role;

-- ============================================================
-- SETUP COMPLETE!
-- ============================================================

-- Summary of what was created:
-- Database: AIFAQ_VERSION1_DB
-- Schema: APP_SCHEMA
-- Warehouse: AIFAQ_WAREHOUSE
-- Tables: DOCUMENTS, CHUNKS, EMBEDDINGS, CHAT_HISTORY