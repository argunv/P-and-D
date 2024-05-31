-- migrate:up

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS patients_full_name_btree_idx ON api_data.patients USING btree (first_name, last_name);

-- CREATE INDEX IF NOT EXISTS patients_last_name_trgm_idx ON api_data.patients USING gin (last_name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS doctors_first_name_btree_idx ON api_data.doctors USING btree (first_name);

CREATE INDEX IF NOT EXISTS doctors_last_name_trgm_idx ON api_data.doctors USING gin (last_name gin_trgm_ops);

-- migrate:down