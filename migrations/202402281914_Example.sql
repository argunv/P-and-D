-- migrate:up

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA api_data;

CREATE TABLE IF NOT EXISTS api_data.doctors (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name TEXT,
    last_name TEXT,
    specialization TEXT
);

CREATE TABLE IF NOT EXISTS api_data.patients (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    gender TEXT
);

CREATE TABLE IF NOT EXISTS api_data.visits (
    patient_id uuid REFERENCES patients,
    doctor_id uuid REFERENCES doctors,
    visit_date DATE,
    diagnosis TEXT
);

INSERT INTO api_data.patients
VALUES 
    (uuid_generate_v4(), 'John', 'Doe', '1990-05-15', 'Male'),
    (uuid_generate_v4(), 'Jane', 'Smith', '1985-10-20', 'Female'),
    (uuid_generate_v4(), 'Michael', 'Johnson', '1978-03-28', 'Male');

INSERT INTO api_data.doctors
VALUES 
    (uuid_generate_v4(), 'Dr. Smith', 'Johnson', 'Cardiologist'),
    (uuid_generate_v4(), 'Dr. Emily', 'Davis', 'Pediatrician'),
    (uuid_generate_v4(), 'Dr. Robert', 'Brown', 'Dermatologist');

INSERT INTO api_data.visits
VALUES 
    ((SELECT id FROM patients WHERE first_name = 'John' AND last_name = 'Doe'), 
     (SELECT id FROM doctors WHERE last_name = 'Johnson'), '2024-03-10', 'High blood pressure'),
    ((SELECT id FROM patients WHERE first_name = 'John' AND last_name = 'Doe'), 
     (SELECT id FROM doctors WHERE last_name = 'Davis'), '2023-11-20', 'Annual checkup');

INSERT INTO api_data.visits
VALUES 
    ((SELECT id FROM patients WHERE first_name = 'Jane' AND last_name = 'Smith'), 
     (SELECT id FROM doctors WHERE last_name = 'Brown'), '2024-02-05', 'Skin rash'),
    ((SELECT id FROM patients WHERE first_name = 'Jane' AND last_name = 'Smith'), 
     (SELECT id FROM doctors WHERE last_name = 'Davis'), '2023-08-15', 'Vaccination');

INSERT INTO api_data.visits
VALUES 
    ((SELECT id FROM patients WHERE first_name = 'Michael' AND last_name = 'Johnson'), 
     (SELECT id FROM doctors WHERE last_name = 'Johnson'), '2024-01-18', 'Heart palpitations'),
    ((SELECT id FROM patients WHERE first_name = 'Michael' AND last_name = 'Johnson'), 
     (SELECT id FROM doctors WHERE last_name = 'Brown'), '2023-10-30', 'Acne treatment');

-- migrate:down