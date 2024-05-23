# SELECT
SELECT_ALL_PATIENTS = """
SELECT * FROM api_data.patients
"""

SELECT_ALL_DOCTORS = """
SELECT * FROM api_data.doctors
"""

# INSERT
INSERT_PATIENT = """
INSERT INTO api_data.patients (first_name, last_name, date_of_birth, gender)
VALUES (%s, %s, %s, %s)
"""

INSERT_DOCTOR = """
INSERT INTO api_data.doctors (first_name, last_name, specialization)
VALUES (%s, %s, %s)
"""

# DELETE
DELETE_PATIENT = """
DELETE FROM api_data.patients WHERE id = %s
"""

DELETE_DOCTOR = """
DELETE FROM api_data.doctors WHERE id = %s
"""

# UPDATE
UPDATE_PATIENT = """
UPDATE api_data.patients
SET {attrs}
WHERE id = %s
"""

UPDATE_DOCTOR = """
UPDATE api_data.doctors
SET {attrs}
WHERE id = %s
"""

# SELECT BY ID
SELECT_PATIENT_BY_ID = """
SELECT * FROM api_data.patients WHERE id = %s
"""

SELECT_DOCTOR_BY_ID = """
SELECT * FROM api_data.doctors WHERE id = %s
"""

# SELECT PATIENTS WITH DOCTORS' VISITS
SELECT_PATIENTS_DOCTORS_VISITS = """
WITH patients_with_doctors AS (
    SELECT
        p.id,
        p.first_name,
        p.last_name,
        p.date_of_birth,
        p.gender,
        coalesce(json_agg(
            json_build_object(
                'id', d.id,
                'first_name', d.first_name,
                'last_name', d.last_name,
                'specialization', d.specialization)
            ) FILTER (WHERE d.id IS NOT NULL), '[]') AS doctors
    FROM
        api_data.patients p
    LEFT JOIN
        api_data.visits v ON p.id = v.patient_id
    LEFT JOIN
        api_data.doctors d ON v.doctor_id = d.id
    GROUP BY
        p.id
),
patients_with_visits AS (
    SELECT
        p.id,
        coalesce(json_agg(
            json_build_object(
                'visit_date', v.visit_date,
                'diagnosis', v.diagnosis)
            ) FILTER (WHERE v.visit_date IS NOT NULL), '[]') AS visits
    FROM
        api_data.patients p
    LEFT JOIN
        api_data.visits v ON p.id = v.patient_id
    GROUP BY
        p.id
)
SELECT
    pwd.id,
    pwd.first_name,
    pwd.last_name,
    pwd.date_of_birth,
    pwd.gender,
    pwd.doctors,
    pwv.visits
FROM
    patients_with_doctors pwd
JOIN
    patients_with_visits pwv ON pwd.id = pwv.id;
"""

# SEARCH PATIENTS
SEARCH_PATIENTS_BOTH = """
SELECT * FROM api_data.patients
WHERE first_name ILIKE %s AND last_name ILIKE %s
"""

SEARCH_PATIENTS_FIRST = """
SELECT * FROM api_data.patients
WHERE first_name ILIKE %s
"""

SEARCH_PATIENTS_LAST = """
SELECT * FROM api_data.patients
WHERE last_name ILIKE %s
"""

# SEARCH DOCTORS
SEARCH_DOCTORS_BOTH = """
SELECT * FROM api_data.doctors
WHERE first_name ILIKE %s AND last_name ILIKE %s
"""

SEARCH_DOCTORS_FIRST = """
SELECT * FROM api_data.doctors
WHERE first_name ILIKE %s
"""

SEARCH_DOCTORS_LAST = """
SELECT * FROM api_data.doctors
WHERE last_name ILIKE %s
"""
