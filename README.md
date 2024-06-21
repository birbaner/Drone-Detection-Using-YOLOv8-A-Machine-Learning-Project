**ASSIGNMENT 2 DOCUMENTATION**

**.ipynb files are my google colab files**
**.npy files where I saved frames**
**.txt file where I saved captions from videos**
**.png files are the first 10 similar images screenshots**
**docker-compose.yml, init.sql, docker-compose.yml, app.py, requirements.txt for Docker and PostgreSQL setup**

**Set up docker compose to bring up two docker containers, your application container with the dev environment (you must have done this in Step 1) and a second container with postgres.**
To index the video images embedding vectors in the PostgreSQL database using the pgvector extension, I used Docker Compose to bring up two containers: one for my application environment and another for PostgreSQL. I pulled the latest PostgreSQL image (`postgres:latest`) and configured it to accept connections from my application container. 

After setting up the database, I processed all detected object sub-images for each frame of the videos to compile the results into a structured table containing fields like `vidId`, `frameNum`, `timestamp`, `detectedObjId`, `detectedObjClass`, `confidence`, `bbox info`, `vector`, and any optional fields. 

I indexed these embedding vectors in the database using the pgvector extension, which supports efficient similarity search operations. I then demonstrated the functionality by querying the database with image vectors and obtaining results that include the first 10 similar images across the input videos.

For a visual demonstration, here are **screenshots showcasing the search results from the PostgreSQL database query,** displaying the first 10 similar images across the input videos **(please find .png files)**. These screenshots validate that the indexing and search operations using image embeddings in PostgreSQL with pgvector were successful and effective. Different .png files shows different search order.

**Here's a summary of what was used:**
Dockerfile, init.sql, docker-compose.yml, app.py, requirements.txt

**From My Code Documentation**
In this script, the goal is to download YouTube videos and their closed captions, preprocess the videos to extract frames, perform object detection using YOLOv5 to identify objects within those frames, crop and save detected objects, and finally, use an autoencoder to extract embeddings from the cropped objects. These embeddings are then stored in a PostgreSQL database with a vector extension for efficient similarity search. Indexing is applied to enhance query performance, and a query mechanism allows retrieval of similar video segments based on the embeddings. The process is encapsulated within comprehensive error handling and logging to ensure robustness throughout each stage of video processing, embedding extraction, and database interaction.

The workflow begins with an autoencoder designed in Keras for compressing 64x64 cropped objects into a lower-dimensional representation, evaluated via PSNR. Following this, embeddings from each frame are stored in detection_results_with_embeddings.csv, with video embeddings subsequently loaded into a PostgreSQL database (video_embeddings table) using psycopg2. A query mechanism based on vector similarity retrieves frames from the database, supported by a function (load_frame) for loading and visualizing results directly from video files. (**please find the .png files)**)

**In the process, frames were saved in a .npy file, captions were stored in a .txt file, detection results along with embeddings were recorded in detection_results_with_embeddings.csv, and video embeddings were stored for efficient retrieval and similarity assessment.**

**For Extra Credi Question**
The provided code implements a Siamese Self-Supervised Learning (SSL) framework to extract meaningful embeddings from preprocessed video frames. Utilizing a ResNet50-based Siamese architecture, frames are processed in pairs to learn and compute cosine similarity between their embeddings, optimizing with mean squared error loss over 50 epochs. Following SSL training, the learned embeddings are extracted and used to detect scene boundaries in videos. By calculating differences between consecutive embeddings and applying normalization and thresholding techniques, the code identifies significant changes in content, effectively delineating scene transitions. This approach demonstrates leveraging SSL for robust video content analysis, facilitating tasks like scene segmentation with learned semantic representations.

