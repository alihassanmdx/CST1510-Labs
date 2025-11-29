import pandas as pd
def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO cyber_incidents
                (date, incident_type, severity, status, description, reported_by)
            VALUES 
                (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (date, incident_type, severity, status, description, reported_by))
        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        print(f"Error inserting incident: {e}")
        return None


def get_all_incidents(conn):
    try:
        return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    except Exception as e:
        print(f"Error retrieving incidents: {e}")
        return pd.DataFrame()


def update_incident_status(conn, incident_id, new_status):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cyber_incidents SET status = ? WHERE id = ?",
            (new_status, incident_id)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error updating incident: {e}")
        return 0


def delete_incident(conn, incident_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM cyber_incidents WHERE id = ?",
            (incident_id,)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error deleting incident: {e}")
        return 0


def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_high_severity_by_status(conn):
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)

def get_incident_types_with_many_cases(conn, min_count=5):
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn, params=(min_count,))


def insert_incident_from_df(conn, df):
    cursor = conn.cursor()
    count = 0

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT OR IGNORE INTO cyber_incidents
            (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["date"],
                row["incident_type"],
                row["severity"],
                row["status"],
                row["description"],
                row.get("reported_by", None)
            )
        )
        count += 1

    conn.commit()
    return count
