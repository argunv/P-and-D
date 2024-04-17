from datetime import datetime
import re

from config import DB_KEYS, UUID_MASK


def UUID(id: str) -> bool:
    """Validate if the provided ID follows the UUID format.

    Args:
        id (str): The ID to be validated.

    Returns:
        bool: True if the ID is valid, False otherwise.
    """
    if not isinstance(id, str):
        return False
    uuid_pattern = re.compile(UUID_MASK)
    return bool(uuid_pattern.match(id))


def patient(data: dict) -> bool:
    """Validate patient data.

    Args:
        data (dict): Patient data to be validated.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not isinstance(data, dict) or not all(key in data for key in DB_KEYS['patients']):
        return False
    if not isinstance(data['first_name'], str) or not isinstance(data['last_name'], str):
        return False
    if not isinstance(data['date_of_birth'], str):
        return False
    try:
        datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    except ValueError:
        return False
    if data['gender'] not in ['Male', 'Female']:
        return False
    return True


def doctor(data: dict) -> bool:
    """Validate doctor data.

    Args:
        data (dict): Doctor data to be validated.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not isinstance(data, dict) or not all(key in data for key in DB_KEYS['doctors']):
        return False
    if not isinstance(data['first_name'], str) or not isinstance(data['last_name'], str):
        return False
    if not isinstance(data['specialty'], str):
        return False
    return True


def visit(data: dict) -> bool:
    """Validate visit data.

    Args:
        data (dict): Visit data to be validated.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not isinstance(data, dict) or not all(key in data for key in DB_KEYS['visits']):
        return False
    if not isinstance(data['patient_id'], str) or not isinstance(data['doctor_id'], str):
        return False
    if not isinstance(data['date'], str):
        return False
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return False
    return True


def medical_record(data: dict) -> bool:
    """Validate medical record data.

    Args:
        data (dict): Medical record data to be validated.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not isinstance(data, dict) or not all(key in data for key in DB_KEYS['medical_records']):
        return False
    if not isinstance(data['patient_id'], str) or not isinstance(data['record'], str):
        return False
    return True


def new_doctor(data: dict) -> bool:
    """Validate new doctor data.

    Args:
        data (dict): New doctor data to be validated.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not isinstance(data, dict) or not any(key in data for key in DB_KEYS['doctors']):
        return False
    if 'specialty' in data and not isinstance(data['specialty'], str):
        return False
    return True


def new_patient(data: dict) -> bool:
    """Validate new patient data.

    Args:
        data (dict): New patient data to be validated.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not isinstance(data, dict) or not any(key in data for key in DB_KEYS['patients']):
        return False
    if 'gender' in data and data['gender'] not in ['Male', 'Female']:
        return False
    return True
