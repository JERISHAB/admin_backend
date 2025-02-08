ALTER TABLE users ADD COLUMN role VARCHAR(10) CHECK (role IN ('admin', 'editor', 'user')) DEFAULT 'user' NOT NULL;
