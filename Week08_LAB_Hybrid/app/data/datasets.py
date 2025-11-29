import pandas as pd

def insert_dataset(conn, dataset_name, category=None, source=None, last_updated=None, record_count=None, file_size_mb=None):
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO datasets_metadata
            (dataset_name, category, source, last_updated, record_count, file_size_mb)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            dataset_name,
            category,
            source,
            last_updated,
            record_count,
            file_size_mb
        ))

        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error inserting dataset: {e}")
        return None


def get_all_datasets(conn):
    try:
        return pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    except Exception as e:
        print(f"Error fetching datasets: {e}")
        return pd.DataFrame()


def update_dataset_count(conn, dataset_id, new_count):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE datasets_metadata SET record_count = ? WHERE id = ?",
            (new_count, dataset_id)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error updating dataset: {e}")
        return 0


def delete_dataset(conn, dataset_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM datasets_metadata WHERE id = ?",
            (dataset_id,)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error deleting dataset: {e}")
        return 0


def get_dataset_count_by_category(conn):
    query = """
    SELECT category, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY category
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_large_datasets(conn, min_size=100):
    query = """
    SELECT *
    FROM datasets_metadata
    WHERE file_size_mb > ?
    ORDER BY file_size_mb DESC
    """
    return pd.read_sql_query(query, conn, params=(min_size,))


def insert_dataset_from_df(conn, df):
    cursor = conn.cursor()
    count = 0

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT OR IGNORE INTO datasets_metadata
            (dataset_name, category, source, last_updated, record_count, file_size_mb)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["dataset_name"],
                row.get("category", None),
                row.get("source", None),
                row.get("last_updated", None),
                row.get("record_count", None),
                row.get("file_size_mb", None)
            )
        )
        count += 1

    conn.commit()
    return count