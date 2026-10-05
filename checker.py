from db import get_connection


def run_checks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Delete old findings so running twice does not create duplicates
            cur.execute("DELETE FROM findings;")

            cur.execute(
                "SELECT name, id, sql_query FROM rules WHERE active = TRUE ORDER BY id;"
            )
            active_rules = cur.fetchall()

            results = {}
            for rule_name, rule_id, sql_query in active_rules:
                cur.execute(sql_query)
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
