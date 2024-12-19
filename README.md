# dbt-airflow-cosmos

## update the dates 


-- First verify the current data format
SELECT created_at, updated_at 
FROM "raw".listings 
LIMIT 5;

-- Convert created_at column
ALTER TABLE "raw".listings 
ALTER COLUMN created_at 
TYPE TIMESTAMP USING created_at::timestamp;

-- Convert updated_at column
ALTER TABLE "raw".listings 
ALTER COLUMN updated_at 
TYPE TIMESTAMP USING updated_at::timestamp;

-- Verify the conversion
SELECT created_at, updated_at 
FROM "raw".listings 
LIMIT 5;
