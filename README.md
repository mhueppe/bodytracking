# Body Tracking with MediaPipe and Unity

This project provides a real-time body tracking solution leveraging MediaPipe and OpenCV, designed to send pose landmark data to a Unity application for seamless integration and visualization with arbitrary humanoid avatars.

## Table of Contents

- [Body Tracking with MediaPipe and Unity](#body-tracking-with-mediapipe-and-unity)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Description

The `bodytracking` repository presents a system for real-time human body movement tracking. It utilizes computer vision techniques with OpenCV and MediaPipe to detect hand gestures, facial expressions, and various body postures. The core functionality involves efficient video capture and pose estimation through multithreading, with the resulting pose landmarks being transmitted to a Unity environment via a named pipe for real-time visualization and control of avatars.

## Features

*   **Real-time Body Tracking:** Detects and tracks human pose, hands, and facial landmarks in real-time.
*   **MediaPipe Integration:** Leverages Google's MediaPipe for robust and accurate pose estimation.
*   **OpenCV Utilization:** Employs OpenCV for video processing and computer vision tasks.
*   **Multithreaded Performance:** Uses multithreading for efficient video capture and pose estimation, enhancing real-time performance.
*   **Unity Integration:** Transmits pose landmark data to a Unity application for visualization and avatar control via a named pipe.
*   **Potential Applications:** Can be used for gesture recognition, fitness analysis, virtual reality interactions, and potentially as a component in intelligent security systems.

## Technologies Used

*   **Python:** The primary programming language for the backend tracking logic.
*   **MediaPipe:** For high-fidelity body, hand, and face landmark detection.
*   **OpenCV:** For camera access, image processing, and other computer vision utilities.
*   **NumPy:** Essential for numerical operations, especially with array manipulation of landmark data.
*   **Unity:** The platform for 3D visualization and avatar integration.

## Installation

To set up the project, follow these steps:

1.  **Install Python:**
    Download and install Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Install Unity:**
    Download and install Unity Hub and then Unity Editor from the official website: [https://unity.com/download](https://unity.com/download)

3.  **Clone the Repository:**
    ```bash
    git clone https://github.com/mhueppe/bodytracking.git
    cd bodytracking
    ```
    Alternatively, you can download the repository as a ZIP file and extract it.

4.  **Install Python Dependencies:**
    Open your terminal or command prompt, navigate to the cloned repository's directory, and install the required Python libraries:
    ```bash
    pip install mediapipe opencv-python numpy
    ```
    *   `mediapipe`: For body tracking functionalities.
    *   `opencv-python`: For computer vision operations.
    *   `numpy`: For numerical processing.

## Usage

To run the body tracking system and visualize it in Unity:

1.  **Start the Python Script:**
    Open a terminal or command prompt in the `bodytracking` directory and run the main Python script:
    ```bash
    python main.py
    ```
    This will initiate the camera feed and MediaPipe processing, and start sending data. A window should open displaying the tracked body. The script will indicate that it's "waiting for Unity project to run."

2.  **Open and Run the Unity Project:**
    *   Open Unity Hub.
    *   Click on "Open" and navigate to the `bodytracking` directory. Select the Unity project folder (e.g., `Unity Media Pipe avatar` if present, or the main `bodytracking` folder itself).
    *   Once the Unity project is open, press the "Play" button in the Unity Editor.

    The Unity application should now connect to the Python script and begin receiving real-time body tracking data, which will drive the integrated avatar or visualization.

## Contributing

Contributions to this project are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## License

The licensing for this specific repository (mhueppe/bodytracking) is not explicitly defined in the provided information.
