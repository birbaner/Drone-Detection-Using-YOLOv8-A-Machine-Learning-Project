-- Create the database
CREATE DATABASE mydatabase;

-- Connect to the database
\c mydatabase;

-- Install the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create your table for storing embeddings
CREATE TABLE IF NOT EXISTS video_embeddings (
    vidId INT,
    frameNum INT,
    timestamp TEXT,
    detectedObjId INT,
    detectedObjClass TEXT,
    confidence FLOAT,
    bbox_info TEXT,
    vector vector(512)  -- Assuming embedding size of 512
);

-- Create an index for fast searching
CREATE INDEX IF NOT EXISTS video_embeddings_vector_idx ON video_embeddings USING ivfflat(vector);
