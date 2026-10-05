ALTER TABLE rules
    ADD COLUMN sql_query TEXT,
    ADD COLUMN active BOOLEAN DEFAULT TRUE;

UPDATE rules
SET sql_query = $$
SELECT id FROM work_records
WHERE status = 'done'
  AND (evidence_link IS NULL OR TRIM(evidence_link) = '');
$$
WHERE name = 'missing_evidence';

UPDATE rules
SET sql_query = $$
SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (
        PARTITION BY va_name, client, task
        ORDER BY id ASC
    ) AS rn
    FROM work_records
) sub
WHERE rn > 1;
$$
WHERE name = 'duplicate_task';

UPDATE rules
SET sql_query = $$
SELECT id FROM work_records
WHERE completed_at > due_at;
$$
WHERE name = 'sla_breach';
