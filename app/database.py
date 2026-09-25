import sqlite3

from app.config import DATABASE_PATH


def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prior_auth_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            treatment TEXT NOT NULL,
            insurer TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def create_request(
    patient_id: str,
    treatment: str,
    insurer: str,
    status: str = "CREATED"
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO prior_auth_requests
        (patient_id, treatment, insurer, status)
        VALUES (?, ?, ?, ?)
        """,
        (
            patient_id,
            treatment,
            insurer,
            status
        )
    )

    connection.commit()

    request_id = cursor.lastrowid

    connection.close()

    return request_id
