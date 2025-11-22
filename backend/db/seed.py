import json
import sys
from pathlib import Path

# Add parent directory to path for imports when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import get_sync_connection


def seed_database():
    """Seed the database with test data from JSON files."""
    data_dir = Path(__file__).parent.parent / "data"

    with get_sync_connection() as conn:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE data_request, request_source CASCADE")

            # Load and insert request_sources
            with open(data_dir / "request_sources.json") as f:
                request_sources = json.load(f)

            for source in request_sources:
                cur.execute(
                    "INSERT INTO request_source (id, name) VALUES (%s, %s)",
                    (source["id"], source["name"]),
                )

            # Load and insert data_requests
            with open(data_dir / "data_requests.json") as f:
                data_requests = json.load(f)

            for request in data_requests:
                cur.execute(
                    """
                    INSERT INTO data_request
                    (id, first_name, last_name, status, created_on, created_by, request_source_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        request["id"],
                        request["firstName"],
                        request["lastName"],
                        request["status"],
                        request["createdOn"],
                        request["createdBy"],
                        request["requestSourceId"],
                    ),
                )

            # Reset the sequence to continue from the max id
            cur.execute(
                "SELECT setval('data_request_id_seq', (SELECT MAX(id) FROM data_request))"
            )

        conn.commit()
        print(f"Seeded {len(request_sources)} request sources")
        print(f"Seeded {len(data_requests)} data requests")


if __name__ == "__main__":
    seed_database()
