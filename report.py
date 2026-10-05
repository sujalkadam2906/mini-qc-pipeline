import argparse
from collections import Counter
from db import get_connection


def generate_report(client=None):
    query = """
        SELECT
            r.name AS rule_name,
            w.client,
            w.va_name,
            w.task,
            w.id AS record_id
        FROM findings f
        JOIN work_records w ON f.record_id = w.id
        JOIN rules r ON f.rule_id = r.id
    """
    params = ()
    if client:
        query += " WHERE w.client = %s"
        params = (client,)

    query += " ORDER BY w.client, w.id, r.name;"

    client_counts = Counter()
    total_findings = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params if params else None)
            rows = cur.fetchall()

    for rule_name, row_client, va_name, task, record_id in rows:
        print(f"[{rule_name}] {row_client} | {va_name} | {task} ({record_id})")
        client_counts[row_client] += 1
        total_findings += 1

    print("\nFindings per client:")
    for row_client, count in sorted(client_counts.items()):
        print(f"  {row_client}: {count}")

    print(f"\nGrand total: {total_findings}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate QC findings report.")
    parser.add_argument("--client", type=str, default=None, help="Filter findings by client")
    args = parser.parse_args()

    generate_report(client=args.client)
