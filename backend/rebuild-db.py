#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(Path(__file__).parent / ".env")


def initialize_database():
    """Run setup_db.sql to create the database."""
    db_dir = Path(__file__).parent / "db"
    setup_script = db_dir / "setup_db.sql"

    result = subprocess.run(
        ["psql", "-U", os.getenv("DB_USER", "postgres"), "-f", str(setup_script)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Database initialization failed:")
        print(result.stderr)
        sys.exit(1)

    print("Database initialized successfully")


def run_flyway_clean_migrate():
    """Run Flyway clean and migrate."""
    db_dir = Path(__file__).parent / "db"

    # Pass DB environment variables to Flyway
    env = os.environ.copy()

    result = subprocess.run(
        ["flyway", "-configFiles=flyway.conf", "clean", "migrate"],
        cwd=db_dir,
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        print("Flyway clean migrate failed:")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)


def seed_database():
    """Run the seed script."""
    from db.seed import seed_database as run_seed

    run_seed()


def main():
    parser = argparse.ArgumentParser(description="Rebuild the database")
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="Run setup_db.sql to create the database (first-time setup)",
    )
    args = parser.parse_args()

    print("=== Rebuilding Database ===\n")

    if args.initialize:
        print("1. Initializing database...")
        initialize_database()
        print()

    print("2. Running flyway clean migrate...")
    run_flyway_clean_migrate()

    print("3. Seeding database...")
    seed_database()

    print("\n=== Database rebuild complete ===")


if __name__ == "__main__":
    main()
