**ASSIGNMENT 2 DOCUMENTATION**

**Set up docker compose to bring up two docker containers, your application container with the dev environment (you must have done this in Step 1) and a second container with postgres.**

To index the video images embedding vectors in the PostgreSQL database using the pgvector extension, I used Docker Compose to bring up two containers: one for my application environment and another for PostgreSQL. I pulled the latest PostgreSQL image (`postgres:latest`) and configured it to accept connections from my application container. 

After setting up the database, I processed all detected object sub-images for each frame of the videos to compile the results into a structured table containing fields like `vidId`, `frameNum`, `timestamp`, `detectedObjId`, `detectedObjClass`, `confidence`, `bbox info`, `vector`, and any optional fields. 

I indexed these embedding vectors in the database using the pgvector extension, which supports efficient similarity search operations. I then demonstrated the functionality by querying the database with image vectors and obtaining results that include the first 10 similar images across the input videos.

For a visual demonstration, here are **screenshots showcasing the search results from the PostgreSQL database query,** displaying the first 10 similar images across the input videos **(please find .png files)**. These screenshots validate that the indexing and search operations using image embeddings in PostgreSQL with pgvector were successful and effective. Different .png files shows different search order.

**Here's a summary of what was used:**

Dockerfile, init.sql, docker-compose.yml, app.py, requirements.txt

