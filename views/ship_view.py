import sqlite3
import json

def update_ship(id, ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Ship
                SET
                    name = ?,
                    hauler_id = ?
            WHERE id = ?
            """,
            (ship_data['name'], ship_data['hauler_id'], id)
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False

def delete_ship(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Ship WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_ships(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        ships = []

        if "_expand" in url["query_params"] and "haulers" in url["query_params"]["_expand"]:
            db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.hauler_id,
                    h.id haulerId,
                    h.name haulerName,
                    h.dock_id
                FROM Ship s
                JOIN Hauler h ON h.id = s.hauler_id
            """)
            query_results = db_cursor.fetchall()

            for row in query_results:
                hauler = {
                    "id": row["haulerId"],
                    "name": row["haulerName"],
                    "dock_id": row["dock_id"]
                }
                ship = {
                    "id": row["id"],
                    "name": row["name"],
                    "hauler_id": row["hauler_id"],
                    "hauler": hauler
                }
                ships.append(ship)
        else:
            db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.hauler_id
                FROM Ship s
            """)
            query_results = db_cursor.fetchall()

            for row in query_results:
                ships.append(dict(row))

        serialized_ships = json.dumps(ships)
        return serialized_ships

def retrieve_ship(pk, url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want

        ships = []

        if "_expand" in url["query_params"] and "haulers" in url["query_params"]["_expand"]:
            db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.hauler_id,
                    h.id haulerId,
                    h.name haulerName,
                    h.dock_id
                FROM Ship s
                JOIN Hauler h ON h.id = s.hauler_id
                WHERE s.id = ?
            """, (pk,))
            row = db_cursor.fetchone()
        else: 
            return json.dumps({"error"})

        if row is not None:
                hauler = {
                    "id": row["haulerId"],
                    "name": row["haulerName"],
                    "dock_id": row["dock_id"]
                }
                ship = {
                    "id": row["id"],
                    "name": row["name"],
                    "hauler_id": row["hauler_id"],
                    "hauler": hauler
                }
                return json.dumps(ship)
        else: 
            db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.hauler_id
        FROM Ship s
        WHERE s.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        dictionary_version_of_object = dict(query_results)
        serialized_ship = json.dumps(dictionary_version_of_object)

    return serialized_ship


def create_ship(ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()


        db_cursor.execute("""
            INSERT INTO Ship (name, hauler_id) 
            VALUES (?, ?)
        """, (ship_data["name"], ship_data["hauler_id"]))

        new_id = db_cursor.lastrowid

        ship_data["id"] = new_id
        return ship_data


