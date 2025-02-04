# Train Derailment Detection

This project is a Python-based program designed to analyze video footage of trains running their routes and assess the risk of derailment. By determining whether a train is turning, the program displays a colored signal indicating the level of risk. If there is a risk of derailment, a **yellow circle** will appear. If no risk is detected, a **green circle** will be displayed.

## Features

- **Video Analysis**  
  Processes input video footage to identify potential derailment risks based on train movement patterns.
  
- **Risk Indicators**  
  - **Yellow Circle**: Indicates a potential risk of derailment.
  - **Green Circle**: Indicates no risk detected.

- **Advanced Image Processing**  
  Utilizes techniques such as edge detection, region masking, and Hough Line Transformation for accurate analysis.

- **Real-Time Processing**  
  Analyzes video frames in real-time and overlays visual indicators on the video output.

## Technical Details

- **Libraries Used**:
  - `argparse`: For handling command-line arguments.
  - `cv2` (OpenCV): For image and video processing.
  - `numpy`: For numerical computations.
  - `math`: For slope calculations and other mathematical operations.

- **Key Methods**:
  - `region_of_interest`: Masks irrelevant parts of the frame to focus on the area of interest.
  - `draw_lines`: Draws detected lines and overlays them on the video frame.
  - `pipeline`: The main function for processing each frame, detecting lines, and determining risk levels.

- **Hough Line Transformation**: Used to detect lines in the masked region of interest.
- **Canny Edge Detection**: Identifies edges in the grayscale image for line detection.

## File Descriptions

- **train.py**  
  The main Python script that processes input videos, analyzes train movement, and displays risk indicators. It includes:
  - Command-line argument handling for specifying input video files.
  - Video frame processing pipeline with real-time visualization.

- **README.md**  
  Provides an overview of the project, its features, file descriptions, and usage instructions.

## How to Use

1. Clone this repository to your local machine:
git clone https://github.com/muditm006/Train-Derailment-Detection.git
cd Train-Derailment-Detection

2. Install the required Python libraries:
pip install numpy opencv-python

3. Run the program with an input video file:
python train.py --video in path/to/your/video.mov

4. View the processed video output with colored signals indicating derailment risks:
- Green circle: No risk detected.
- Yellow circle: Potential derailment risk.

5. Modify or extend functionality by editing the provided Python script as needed.

## Notes

This project demonstrates real-time video analysis using Python's OpenCV library and advanced image processing techniques. It is designed to provide insights into train safety by identifying potential derailment risks.
