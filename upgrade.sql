-- Running upgrade 634a8a7a9c98 -> 66419ca24d01

ALTER TABLE user_preferences DROP COLUMN user_id;

ALTER TABLE user_preferences DROP COLUMN preferences;

ALTER TABLE user_preferences ADD COLUMN name VARCHAR NOT NULL;

ALTER TABLE user_preferences ADD COLUMN job_title VARCHAR NOT NULL;

ALTER TABLE user_preferences ADD COLUMN location VARCHAR NOT NULL;

ALTER TABLE user_preferences ADD COLUMN skills VARCHAR NOT NULL;

ALTER TABLE user_preferences ADD COLUMN whatsapp_number VARCHAR NOT NULL;

UPDATE alembic_version SET version_num='66419ca24d01' WHERE alembic_version.version_num = '634a8a7a9c98';

COMMIT;