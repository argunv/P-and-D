-- migrate:up

-- Ensure the extension is available before using it in the index creation
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Adding a btree index to the first_name column of the patients table
CREATE INDEX IF NOT EXISTS patients_first_name_btree_idx ON api_data.patients USING btree (first_name);

-- Adding a trigram index to the last_name column of the patients table
CREATE INDEX IF NOT EXISTS patients_last_name_trgm_idx ON api_data.patients USING gin (last_name gin_trgm_ops);

-- Adding a btree index to the first_name column of the doctors table
CREATE INDEX IF NOT EXISTS doctors_first_name_btree_idx ON api_data.doctors USING btree (first_name);

-- Adding a trigram index to the last_name column of the doctors table
CREATE INDEX IF NOT EXISTS doctors_last_name_trgm_idx ON api_data.doctors USING gin (last_name gin_trgm_ops);

-- migrate:down