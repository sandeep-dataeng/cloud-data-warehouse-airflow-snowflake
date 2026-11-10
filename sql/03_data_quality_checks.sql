-- Run after loading STG_CUSTOMER. Each query should return zero rows
-- (or be handled by an explicit rejection policy) before dimension processing.

-- Missing required identifiers or attributes.
SELECT *
FROM STG_CUSTOMER
WHERE CUSTOMER_ID IS NULL
   OR TRIM(CUSTOMER_ID) = ''
   OR CUSTOMER_NAME IS NULL
   OR UPDATED_AT IS NULL;

-- Duplicate customer keys within the same batch.
SELECT BATCH_ID, CUSTOMER_ID, COUNT(*) AS ROW_COUNT
FROM STG_CUSTOMER
GROUP BY BATCH_ID, CUSTOMER_ID
HAVING COUNT(*) > 1;

-- Invalid email values (basic illustrative check, not full RFC validation).
SELECT *
FROM STG_CUSTOMER
WHERE EMAIL IS NOT NULL
  AND EMAIL NOT LIKE '%_@_%._%';
