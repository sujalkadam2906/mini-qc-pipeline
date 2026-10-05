from db import get_connection


def run_checks():
    rules_to_check = [
        "missing_evidence",
        "duplicate_task",
        "sla_breach",
    ]

    rule_queries = {
        "missing_evidence": """
            SELECT id FROM work_records
            WHERE status = 'done'
              AND (evidence_link IS NULL OR TRIM(evidence_link) = '');
        """,
        "duplicate_task": """
            SELECT id FROM (
                SELECT id, ROW_NUMBER() OVER (
                    PARTITION BY va_name, client, task
                    ORDER BY id ASC
                ) AS rn
                FROM work_records
            ) sub
            WHERE rn > 1;
        """,
        "sla_breach": """
            SELECT id FROM work_records
            WHERE completed_at > due_at;
        """,
    }

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Delete old findings so running twice does not create duplicates
            cur.execute("DELETE FROM findings;")

            # Look up each rule's id from the rules table by name
            cur.execute("SELECT name, id FROM rules;")
            rule_id_map = dict(cur.fetchall())

            results = {}
            for rule_name in rules_to_check:
                rule_id = rule_id_map.get(rule_name)
                if rule_id is None:
                    raise ValueError(f"Rule '{rule_name}' not found in rules table.")

                cur.execute(rule_queries[rule_name])
                record_ids = [row[0] for row in cur.fetchall()]

                if record_ids:
                    findings_data = [(rec_id, rule_id) for rec_id in record_ids]
                    cur.executemany(
                        "INSERT INTO findings (record_id, rule_id) VALUES (%s, %s);",
                        findings_data,
                    )

                results[rule_name] = len(record_ids)

        conn.commit()

    for rule_name, count in results.items():
        print(f"{rule_name}: {count}")

    return results


if __name__ == "__main__":
    run_checks()
