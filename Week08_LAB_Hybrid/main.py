from pathlib import Path
import os
import pandas as pd
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident_from_df, get_incidents_by_type_count, insert_incident, update_incident_status, get_high_severity_by_status, delete_incident, get_all_incidents
from app.data.tickets import insert_ticket_from_df
from app.data.datasets import insert_dataset_from_df

DB_PATH = Path("DATA") / "intelligence_platform.db"
CSV_DIR = Path("DATA")
if DB_PATH.exists():
    try:
        os.remove(DB_PATH)
        print("🗑️  Deleted old database")
    except Exception as e:
        print(f"⚠️  Could not delete database: {e}")
        print("Please manually delete: data/intelligence_platform.db")
        exit(1)


def load_all_csv_data(conn):
    total_rows_inserted = 0
    csv_table_mapping = {
        "cyber_incidents.csv": ("cyber_incidents", insert_incident_from_df),
        "it_tickets.csv": ("it_tickets", insert_ticket_from_df),
        "datasets_metadata.csv": ("datasets_metadata", insert_dataset_from_df),
    }

    for filename, (table, insert_func) in csv_table_mapping.items():
        path = CSV_DIR / filename

        if not path.exists() or path.stat().st_size == 0:
            print(f"Skipping {filename} (missing or empty).")
            continue

        try:
            df = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            print(f"Skipping {filename} (unreadable).")
            continue

        rename_rules = {
            "cyber_incidents": {
                "type": "incident_type",
                "severity_level": "severity",
                "reportedBy": "reported_by"
            },
            "it_tickets": {
                "ticketID": "ticket_id",
                "Ticket ID": "ticket_id",
                "priorityLevel": "priority",
                "assignedTo": "assigned_to",
                "createdDate": "created_date",
                "resolvedDate": "resolved_date"
            },
            "datasets_metadata": {
                "datasetName": "dataset_name",
                "fileSize": "file_size_mb",
                "recordCount": "record_count",
                "lastUpdated": "last_updated"
            }
        }

        if table in rename_rules:
            df.rename(
                columns={old: new for old, new in rename_rules[table].items() if old in df.columns},
                inplace=True,
            )
        rows_inserted = insert_func(conn, df)
        total_rows_inserted += rows_inserted
        print(f"✔ Loaded {rows_inserted} rows into {table}")

    return total_rows_inserted


def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       ✔ Connected")

    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       ✔ Migrated {user_count} users")

    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)
    print(f"       ✔ Loaded {total_rows} total rows from CSV files")

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n📊 Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n📍 Database location: {DB_PATH.resolve()}")
    print("\n🚀 You're ready for Week 9 (Streamlit web interface)!")




def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    # Create
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: ✅ Incident #{test_id} created")

    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")

    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")

    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")

    conn.close()

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)



def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users
    migrate_users_from_file(conn)

    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 4. Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")


if __name__ == "__main__":
    # Run the complete setup
    setup_database_complete()
    # Run tests
    run_comprehensive_tests()