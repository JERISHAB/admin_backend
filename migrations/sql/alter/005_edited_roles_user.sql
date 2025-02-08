ALTER TABLE users ADD COLUMN role VARCHAR(10) CHECK (role IN ('admin', 'editor','viewer')) DEFAULT 'viewer' NOT NULL;
