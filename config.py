DB_KEYS = {
    'patients': ["first_name", "last_name", "date_of_birth", "gender"],
    'doctors': ["first_name", "last_name", "specialization"],
    'visits': ["patient_id", "visit_date", "diagnosis"]
}
UUID_MASK = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
MAX_CONN = 1
MIN_CONN = 10
