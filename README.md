# AI Proctoring System

A robust, real-time AI-based proctoring solution designed to monitor exam integrity using computer vision.

## Features

-   **Real-time Face Detection**: Monitors the candidate's presence and visibility.
-   **Infraction Detection**: Automatically flags suspicious behavior such as:
    -   Multiple faces detected.
    -   No face detected (candidate left the screen).
-   **Stabilized Monitoring**: Includes an intelligent buffer to prevent false alarms from momentary glitches or lighting changes.
-   **Trust Score**: A dynamic trust metric that decreases based on detected infractions.
-   **Premium UI**: A modern, glassmorphism-inspired interface with dark mode and smooth animations.
-   **Event Logging**: Detailed side-panel log of all monitoring events.

## Tech Stack

-   **Backend**: Python, Flask, Flask-SocketIO
-   **Computer Vision**: OpenCV (Haar Cascades for efficiency)
-   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript

## Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ai-proctoring-system.git
    cd ai-proctoring-system
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python app.py
    ```

4.  **Access the dashboard**:
    Open your browser and navigate to `http://127.0.0.1:5000`.

## Configuration

-   **Detection Sensitivity**: Adjustable via `engine.py` (ProctorEngine class).
-   **Buffer Threshold**: The buffer size for infraction persistence can be tuned in `engine.py`.

## License

MIT License.
