
# ROADWATCH

 detecting and classifying vehicles on roads


## PROBLEM STATEMENT

The problem statement addressed by this proposed project is the lack of an efficient and accurate system for detecting and classifying vehicles on roads. The existing methods for vehicle detection are often manual, time-consuming, and prone to errors. The current approaches involve human intervention and require extensive manual labor, leading to low accuracy and high error rates. Moreover, the lack of real-time monitoring and analysis of vehicle data poses a significant challenge in effective traffic control and targeted advertising


## PROJECT REPORT

[Documentation](https://drive.google.com/file/d/1iYFcArIKSQp5ff8R7JZFwAAhXzoCNGjF/view?usp=sharing)


## RUNNING THE PROJECT

In this repository you can see 2 main programs: `roadwatch_yolov3.py` and `roadwatch_yolov3_custom.py`.

### HOW TO RUN
- Download `.weights` file for YOLO: https://www.kaggle.com/datasets/shivam316/yolov3-weights
- Move `.weights` file to `yolo/` folder
- Go to the project's repository via command line
- type python `roadwatch_yolov3_custom.py -y yolo --input videos/your_test_video_name --output output --skip-frames 5` and hit `Enter`

The proccessed video will be saved to the  `output/` folder.

### Starting the Dashboard
- using `NPM` use command `npm i` to install the required packages.
- use `npm run start` to start the ReactJS Dashboard.
- Once a video is proccessed, and file data is stored in JSON in the `output/` folder, it can be fetched using Project Dashboard.

