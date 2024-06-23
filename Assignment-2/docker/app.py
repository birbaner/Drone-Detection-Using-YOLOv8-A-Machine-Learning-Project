from flask import Flask, request, jsonify
import psycopg2
import cv2
import pandas as pd
import ast
import matplotlib.pyplot as plt

# Initialize Flask app
app = Flask(__name__)

# Function to load a specific frame from a video file
def load_frame(video_path, frame_num):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        print(f"Failed to load frame {frame_num} from {video_path}")
        return None

# Function to query similar embeddings from PostgreSQL
def query_similar_embeddings(query_vector):
    try:
        # Connection details
        host = "localhost"
        database = "mydatabase"
        user = "postgres"
        password = "postgres"

        # Convert the list of floats to a PostgreSQL array string with brackets
        query_vector_str = '[' + ','.join(map(str, query_vector)) + ']'

        # Construct the search query
        search_query = f"""
        SELECT vidId, frameNum, timestamp, detectedObjId, detectedObjClass, confidence, bbox_info, vector,
               vector <-> '{query_vector_str}'::vector AS distance
        FROM video_embeddings
        ORDER BY distance ASC
        LIMIT 10;
        """

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print("Successfully connected to PostgreSQL!")

        # Execute the search query
        with conn.cursor() as cur:
            cur.execute(search_query)
            rows = cur.fetchall()

            # Close connection
            conn.close()

            return rows

    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return None

# Video paths
video_paths = [
    r"C:\Users\user\Desktop\AI_Assignment2\How Green Roofs Can Help Cities _ NPR.mp4",
    r"C:\Users\user\Desktop\AI_Assignment2\What Does 'High-Quality' Preschool Look Like_ _ NPR Ed.mp4",
    r"C:\Users\user\Desktop\AI_Assignment2\Why It’s Usually Hotter In A City _ Let's Talk _ NPR.mp4"
]

# Endpoint to insert embeddings (similar to previous example)
@app.route('/insert_embeddings', methods=['POST'])
def insert_embeddings_route():
    # Insert embeddings logic here if needed
    return jsonify({"message": "Embeddings inserted successfully"}), 200

# Endpoint to query similar embeddings and display frames
@app.route('/query_and_display_frames', methods=['POST'])
def query_and_display_frames_route():
    try:
        # Example of handling POST data
        req_data = request.get_json()
        query_vector = req_data['query_embedding_vector']  # Example of handling query embedding vector from POST request

        # Query similar embeddings
        similar_embeddings = query_similar_embeddings(query_vector)
        if not similar_embeddings:
            return jsonify({"message": "Error querying embeddings"}), 500

        # Display similar frames
        plt.figure(figsize=(20, 10))
        for i, row in enumerate(similar_embeddings):
            if i >= 10:  # Display only the first 10 similar frames
                break

            vidId = row[0]
            frameNum = row[1]
            video_path = video_paths[vidId]

            print(f"Loading frame {frameNum} from video {video_path}")
            frame = load_frame(video_path, frameNum)

            if frame is not None:
                print(f"Frame {frameNum} from video {video_path} loaded successfully with shape: {frame.shape}")
                plt.subplot(2, 5, i+1)
                plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                plt.title(f"Video ID: {vidId}, Frame: {frameNum}")
                plt.axis('off')
            else:
                print(f"Failed to display frame {frameNum} from video {video_path}")

        plt.tight_layout()
        plt.show()

        return jsonify({"message": "Frames displayed successfully"}), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"message": "Error processing request"}), 500

# Main entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
