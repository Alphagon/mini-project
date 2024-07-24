CREATE DATABASE sentiment_db;

\c sentiment_db

Do $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables Where schemaname = 'public' AND tablename = 'predictions') THEN
        CREATE TABLE predictions (
            id SERIAL PRIMARY KEY,
            review_text TEXT,
            predicted_label VARCHAR(10),
            probability FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ELSE
        RAISE NOTICE 'Table predictions already exists'
    END IF;
END $$;