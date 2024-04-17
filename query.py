# SELECT
SELECT_ALL_PATIENTS = """
SELECT * FROM patients
"""

SELECT_ALL_DOCTORS = """
SELECT * FROM doctors
"""

# INSERT
INSERT_PATIENT = """
INSERT INTO patients (first_name, last_name, date_of_birth, gender)
VALUES (%s, %s, %s, %s)
"""

INSERT_DOCTOR = """
INSERT INTO doctors (first_name, last_name, specialization)
VALUES (%s, %s, %s)
"""

# DELETE
DELETE_PATIENT = """
DELETE FROM patients WHERE id = %s
"""

DELETE_DOCTOR = """
DELETE FROM doctors WHERE id = %s
"""

# UPDATE
UPDATE_PATIENT = """
UPDATE patients
SET {attrs}
WHERE id = %s
"""

UPDATE_DOCTOR = """
UPDATE doctors
SET {attrs}
WHERE id = %s
"""

# SELECT BY ID
SELECT_PATIENT_BY_ID = """
SELECT * FROM patients WHERE id = %s
"""

SELECT_DOCTOR_BY_ID = """
SELECT * FROM doctors WHERE id = %s
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
        patients p
    LEFT JOIN
        visits v ON p.id = v.patient_id
    LEFT JOIN
        doctors d ON v.doctor_id = d.id
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
        patients p
    LEFT JOIN
        visits v ON p.id = v.patient_id
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
