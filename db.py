from dotenv import load_dotenv
import os
from typing import Callable

from psycopg2 import pool
from psycopg2.extensions import connection

import query
import validate
from config import DB_KEYS, MIN_CONN, MAX_CONN


class ConnectionPool:
    """A class representing a connection pool to a PostgreSQL database.

    Attributes:
        None

    Methods:
        __init__() -> None:
            Initializes a new ConnectionPool instance and creates a connection pool.

        get_connection() -> connection:
            Gets a connection from the connection pool.

        put_connection(connection: connection) -> None:
            Puts back a connection to the connection pool.

        close_all_connections() -> None:
            Closes all connections in the connection pool.

    """

    def __init__(self) -> None:
        """Initialize a new ConnectionPool instance and create a connection pool."""
        load_dotenv()

        credentials = {
            'host': os.environ.get('PG_HOST', '127.0.0.1'),
            'port': int(os.environ.get('POSTGRES_PORT', '5432')),
            'dbname': os.environ.get('POSTGRES_DB', 'test'),
            'user': os.environ.get('POSTGRES_USER', 'test'),
            'password': os.environ.get('POSTGRES_PASSWORD'),
        }

        self.pool = pool.SimpleConnectionPool(MIN_CONN, MAX_CONN, **credentials)

    def get_connection(self) -> connection:
        """Get a connection from the connection pool.

        Returns:
            connection: A connection from the pool.
        """
        return self.pool.getconn()

    def put_connection(self, connection: connection) -> None:
        """Put back a connection to the connection pool.

        Args:
            connection (connection): The connection to be put back to the pool.
        """
        self.pool.putconn(connection)

    def close_all_connections(self) -> None:
        """Close all connections in the connection pool."""
        self.pool.closeall()


db_pool = ConnectionPool()


def execute_query(query_string: str, values=None) -> bool:
    """Execute a SQL query and commit the changes.

    Args:
        query_string (str): The SQL query string.
        values (tuple, optional): Values to be passed into the query. Defaults to None.

    Returns:
        bool: True if the query executed successfully, False otherwise.
    """
    connection = db_pool.get_connection()

    try:
        with connection.cursor() as cursor:
            if values:
                cursor.execute(query_string, values)
            else:
                cursor.execute(query_string)

            connection.commit()
            result = bool(cursor.rowcount)
    finally:
        db_pool.put_connection(connection)

    return result


def verify(validation_func: Callable) -> Callable:
    """A decorator to verify input data before executing a function.

    Args:
        validation_func (callable): The validation function to be applied.

    Returns:
        callable: The decorator function.
    """
    def decorator(func: Callable) -> Callable:
        """The decorator function.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The decorated function.
        """
        def wrapper(*args, **kwargs):
            """The wrapper function.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Any: The result of the function call if validation passes, False otherwise.
            """
            if not validation_func(*args, **kwargs):
                return False
            return func(*args, **kwargs)
        return wrapper
    return decorator


@verify(validate.UUID)
def delete_patient(id: str) -> bool:
    """Delete a patient from the database.

    Args:
        id (str): ID of the patient.

    Returns:
        bool: True if deletion is successful, False otherwise.
    """
    return execute_query(query.DELETE_PATIENT, (id,))


@verify(validate.UUID)
def delete_doctor(id: str) -> bool:
    """Delete a doctor from the database.

    Args:
        id (str): ID of the doctor.

    Returns:
        bool: True if deletion is successful, False otherwise.
    """
    return execute_query(query.DELETE_DOCTOR, (id,))


@verify(validate.patient)
def add_patient(data: dict) -> bool:
    """Add a new patient to the database.

    Args:
        data (dict): Patient data.

    Returns:
        bool: True if addition is successful, False otherwise.
    """
    values = [data[key] for key in DB_KEYS['api_data.patients']]
    return execute_query(query.INSERT_PATIENT, values)


@verify(validate.doctor)
def add_doctor(data: dict) -> bool:
    """Add a new doctor to the database.

    Args:
        data (dict): Doctor data.

    Returns:
        bool: True if addition is successful, False otherwise.
    """
    values = [data[key] for key in DB_KEYS['api_data.doctors']]
    return execute_query(query.INSERT_DOCTOR, values)


@verify(validate.new_patient)
def update_patient(id: str, new_data: dict) -> bool:
    """Update an existing patient in the database.

    Args:
        id (str): ID of the patient to update.
        new_data (dict): New data for the patient.

    Returns:
        bool: True if update is successful, False otherwise.
    """
    attrs = ', '.join(f'{key}=%s' for key in new_data.keys())
    values = list(new_data.values())
    values.append(id)
    return execute_query(query.UPDATE_PATIENT.format(attrs=attrs), values)


@verify(validate.new_doctor)
def update_doctor(id: str, new_data: dict) -> bool:
    """Update an existing doctor in the database.

    Args:
        id (str): ID of the doctor to update.
        new_data (dict): New data for the doctor.

    Returns:
        bool: True if update is successful, False otherwise.
    """
    attrs = ', '.join(f'{key}=%s' for key in new_data.keys())
    values = list(new_data.values())
    values.append(id)
    return execute_query(query.UPDATE_DOCTOR.format(attrs=attrs), values)


def get_all_patients() -> list:
    """Get all patients from the database.

    Returns:
        list: List of all patients.
    """
    with db_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query.SELECT_ALL_PATIENTS)
            return cursor.fetchall()


def get_all_doctors() -> list:
    """Get all doctors from the database.

    Returns:
        list: List of all doctors.
    """
    with db_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query.SELECT_ALL_DOCTORS)
            return cursor.fetchall()


@verify(validate.UUID)
def get_patient_by_id(id: str) -> tuple:
    """Get a patient by ID from the database.

    Args:
        id (str): ID of the patient.

    Returns:
        tuple: Patient data.
    """
    with db_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query.SELECT_PATIENT_BY_ID, (id,))
            return cursor.fetchone()


@verify(validate.UUID)
def get_doctor_by_id(id: str) -> tuple:
    """Get a doctor by ID from the database.

    Args:
        id (str): ID of the doctor.

    Returns:
        tuple: Doctor data.
    """
    with db_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query.SELECT_DOCTOR_BY_ID, (id,))
            return cursor.fetchone()


def get_patients_with_doctors_visits() -> list:
    """Get all patients with their doctors' visits from the database.

    Returns:
        list: List of patients with their doctors' visits.
    """
    with db_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query.SELECT_PATIENTS_DOCTORS_VISITS)
            return cursor.fetchall()
