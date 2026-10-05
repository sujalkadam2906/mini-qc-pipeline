# Mini QC Pipeline

Mini QC Pipeline is a small quality control pipeline that checks Virtual Assistant (VA) work records in PostgreSQL against rules stored in a rules table. When executed, it evaluates active rules and writes any identified violations into a findings table. A built-in reporting tool aggregates and displays these findings across all clients or filtered by a specific client.

## Setup (Windows)

1. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root directory containing your PostgreSQL connection details:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=mini_qc
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

4. **Create the database and load schema and seed data:**
   Create the `mini_qc` database and load `schema.sql` and `seed.sql` using `psql`:
   ```powershell
   psql -U postgres -c "CREATE DATABASE mini_qc;"
   psql -U postgres -d mini_qc -f schema.sql
   psql -U postgres -d mini_qc -f seed.sql
   ```

## How to Run

1. **Run QC Checks:**
   Clears previous findings, executes all active rules against `work_records`, logs progress to console and `qc.log`, and inserts findings into the database:
   ```powershell
   python checker.py
   ```

2. **Generate Findings Report:**
   Displays all findings grouped by client and work record, with per-client counts and a grand total:
   ```powershell
   python report.py
   ```

3. **Filter Report by Client:**
   Displays findings only for the specified client:
   ```powershell
   python report.py --client Acme
   ```

## Database Tables

- **`work_records`**: Stores Virtual Assistant work log entries, including `id`, `va_name`, `client`, `task`, `status`, `evidence_link`, `due_at`, and `completed_at`.
- **`rules`**: Stores QC validation rules, including `id`, unique rule `name`, human-readable `message`, the check logic in `sql_query`, and an `active` boolean flag.
- **`findings`**: Stores violations identified during QC runs, referencing `record_id` (foreign key to `work_records.id`), `rule_id` (foreign key to `rules.id`), and `created_at`.

## How to Add a New Rule

To add a new rule, perform an `INSERT` into the `rules` table specifying `name`, `message`, and `sql_query`. The `sql_query` **must return record ids in its first column** so the checker can map each violation to its corresponding `work_records` entry.

Example:
```sql
INSERT INTO rules (name, message, sql_query)
VALUES (
    'missing_evidence_pending',
    'In-progress task has no evidence link',
    'SELECT id FROM work_records WHERE status = ''in_progress'' AND (evidence_link IS NULL OR TRIM(evidence_link) = '''');'
);
```

## File List

- **`db.py`**: Provides the database connection helper function (`get_connection`) using credentials loaded from `.env`.
- **`checker.py`**: Runs active QC rules from the `rules` table, logs results to stdout and `qc.log`, and populates the `findings` table.
- **`report.py`**: Generates a formatted summary report of findings with client counts and optional `--client` filtering.
- **`schema.sql`**: PostgreSQL database dump defining table schemas (`work_records`, `rules`, `findings`), constraints, and sequences.
- **`seed.sql`**: Sample dataset containing rules, work records, and sample findings.
- **`migrations/`**: Contains database migration scripts (such as `001_add_rule_sql.sql` which adds `sql_query` and `active` columns to `rules`).
- **`requirements.txt`**: Python dependencies (`psycopg`, `psycopg-binary`, `python-dotenv`, `tzdata`).
- **`README.md`**: Project overview, setup instructions, and operational documentation.
