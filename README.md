**Assignment-3- UAV DETECTION AND TRACKING**
## Setting Up Development Environment and Preparing Dataset

Download and extract the YOLO Drone Detection Dataset from Kaggle. Verify the extraction by listing the contents of the extracted directories, including training and validation images and labels. Display a sample training image and its corresponding label. Correct the `data.yaml` file to specify the paths for training and validation images and ensure it has the correct class information.

## Drone Object Detection

Fine-tune a YOLOv8 model using the drone detection dataset from Kaggle. Split the test videos into frames and use the trained model to detect drones in each frame. Save frames with detected drones to a directory named `detections`. Ensure the code processes multiple videos from a directory, providing real-time drone detection and storing the results in a structured format for post-processing and visualization.
The process includes downloading test videos from YouTube, splitting the videos into frames, and saving frames with detected drones to a directory. The project utilizes YOLOv8 for drone detection, processes multiple videos from a directory, and stores the results in a structured format for post-processing and visualization. The detections are saved in the detections directory for further analysis.

**Please see video files to see the output**

In this project, I implemented a Kalman Filter using the `filterpy` library to track a drone in two video recordings. The process involved extracting frames from the videos, detecting the drone in each frame using pre-existing detections, initializing the Kalman Filter with the initial detection coordinates, and then updating it as new detections became available. The Kalman Filter was configured with parameters such as state transition matrix, measurement function, and noise covariances to optimize tracking performance. The filtered states from the Kalman Filter were used to plot the drone's 2D trajectory across frames, and these trajectories were overlaid on the original video frames for visualization. The final output included short videos where the drone's trajectory was shown as a line connecting its positions indicated by the Kalman Filter, with bounding boxes overlaid to indicate its presence in each frame. This approach enabled accurate tracking and visualization of the drone's movement across both video recordings.


## Comment
Note: Due to GitHub's limitations in rendering .ipynb files with complex code blocks, I have uploaded multiple formats of my code for accessibility. You can download the code in .ipynb, .py, .pdf, and .html formats to view it. Additionally, all output video files are available for download in .mp4 and .png formats. Feel free to choose the format that best suits your needs.
