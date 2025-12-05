import pandas as pd

def insert_ticket(conn, ticket_id, subject, priority, status, category=None,
                  description=None, created_date=None, assigned_to=None):
    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO it_tickets
            (ticket_id, subject, priority, status, category, description, created_date, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            ticket_id,
            subject,
            priority,
            status,
            category,
            description,
            created_date,
            assigned_to
        ))

        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        print(f"Error inserting ticket: {e}")
        return None


def get_all_tickets(conn):
    try:
        return pd.read_sql_query("SELECT * FROM it_tickets", conn)
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return pd.DataFrame()


def update_ticket_status(conn, ticket_id, new_status):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE it_tickets SET status = ? WHERE id = ?",
            (new_status, ticket_id)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error updating ticket: {e}")
        return 0


def delete_ticket(conn, ticket_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM it_tickets WHERE id = ?",
            (ticket_id,)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error deleting ticket: {e}")
        return 0


def get_ticket_count_by_status(conn):
    query = """
    SELECT status, COUNT(*) AS count
    FROM it_tickets
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_high_priority_tickets(conn):
    """
    WHERE + ORDER BY
    """
    query = """
    SELECT * FROM it_tickets
    WHERE priority = 'High'
    ORDER BY created_at DESC
    """
    return pd.read_sql_query(query, conn)


def get_assigned_ticket_counts(conn):
    query = """
    SELECT assigned_to, COUNT(*) as count
    FROM it_tickets
    GROUP BY assigned_to
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def insert_ticket_from_df(conn, df):
    cursor = conn.cursor()
    count = 0

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT OR IGNORE INTO it_tickets
            (ticket_id, subject, priority, status, category, description, created_date, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["ticket_id"],
                row["subject"],
                row["priority"],
                row["status"],
                row.get("category", None),
                row.get("description", None),
                row.get("created_date", None),
                row.get("assigned_to", None)
            )
        )
        count += 1

    conn.commit()
    return count