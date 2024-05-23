-- migrate:up

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO api_data.patients (id, first_name, last_name, date_of_birth, gender)
SELECT 
    uuid_generate_v4(),
    first_names[1 + floor((random() * array_length(first_names, 1)))::int],
    last_names[1 + floor((random() * array_length(last_names, 1)))::int],
    (date '1950-01-01' + (floor(random() * 18262))::int)::date, -- Days between 1950-01-01 and 2000-01-01 (18262)
    CASE WHEN random() > 0.5 THEN 'Male' ELSE 'Female' END
FROM generate_series(1, 100) AS id
CROSS JOIN (
    SELECT 
        '{John,Jane,Michael,Emily,Sophia,William,Olivia,Alexander,Emma,James}'::text[] AS first_names,
        '{Smith,Johnson,Williams,Jones,Brown,Davis,Miller,Wilson,Taylor,Clark}'::text[] AS last_names
) AS nms;

INSERT INTO api_data.doctors (id, first_name, last_name, specialization)
SELECT 
    uuid_generate_v4(),
    first_names[1 + floor((random() * array_length(first_names, 1)))::int],
    last_names[1 + floor((random() * array_length(last_names, 1)))::int],
    CASE floor(random() * 3)
        WHEN 0 THEN 'Cardiologist'
        WHEN 1 THEN 'Pediatrician'
        ELSE 'Dermatologist'
    END
FROM generate_series(1, 50) AS id
CROSS JOIN (
    SELECT 
        '{Dr. Smith,Dr. Johnson,Dr. Williams,Dr. Brown,Dr. Davis,Dr. Miller,Dr. Wilson,Dr. Taylor,Dr. Clark}'::text[] AS first_names,
        '{Ivanov,Smirnov,Kuznetsov,Popov,Vasiliev,Petrov,Sokolov,Mikhailov,Novikov,Fedorov}'::text[] AS last_names
) AS nms;

-- migrate:down
