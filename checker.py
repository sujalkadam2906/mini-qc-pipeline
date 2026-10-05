import logging
import sys
from db import get_connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("qc.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def run_checks():
    logger.info("QC run started")
    results = {}
    failed_rules = []

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Delete old findings so running twice does not create duplicates
            cur.execute("DELETE FROM findings;")

            cur.execute(
                "SELECT name, id, sql_query FROM rules WHERE active = TRUE ORDER BY id;"
            )
            active_rules = cur.fetchall()

        for rule_name, rule_id, sql_query in active_rules:
            try:
                with conn.transaction():
                    with conn.cursor() as cur:
                        cur.execute(sql_query)
                        record_ids = [row[0] for row in cur.fetchall()]

                        if record_ids:
                            findings_data = [(rec_id, rule_id) for rec_id in record_ids]
                            cur.executemany(
                                "INSERT INTO findings (record_id, rule_id) VALUES (%s, %s);",
                                findings_data,
                            )

                results[rule_name] = len(record_ids)
                logger.info(f"Rule '{rule_name}' produced {len(record_ids)} findings")
            except Exception as e:
                logger.error(f"Rule '{rule_name}' failed: {e}")
                failed_rules.append(rule_name)

        conn.commit()

    for rule_name, count in results.items():
        print(f"{rule_name}: {count}")

    total_findings = sum(results.values())
    logger.info(f"QC run finished. Total findings: {total_findings}")

    if failed_rules:
        logger.warning(f"Failed rules: {', '.join(failed_rules)}")
        sys.exit(1)

    return results


if __name__ == "__main__":
    run_checks()

