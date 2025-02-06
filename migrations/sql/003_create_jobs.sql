CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    experience_required INT NOT NULL,
    status VARCHAR(10) CHECK (status IN ('active', 'private', 'closed')) DEFAULT 'active' NOT NULL,
    location VARCHAR(10) CHECK (location IN ('remote', 'hybrid', 'onsite')) NOT NULL,
    timing VARCHAR(10) CHECK (timing IN ('full-time', 'part-time', 'contract')) NOT NULL,
    about TEXT NOT NULL,
    responsibilities TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
