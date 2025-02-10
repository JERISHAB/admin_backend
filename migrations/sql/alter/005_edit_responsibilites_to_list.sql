-- Change the table name if it's different
ALTER TABLE jobs DROP COLUMN responsibilities;

-- Add the new responsibilities column as an array of text
ALTER TABLE jobs ADD COLUMN responsibilities TEXT[];
