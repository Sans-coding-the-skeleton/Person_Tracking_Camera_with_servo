# Person Tracking Camera with Servo

Welcome to the **Person Tracking Camera with Servo** project! 🎥🤖 This project utilizes a camera and servo motor to track moving objects in a predefined field.

## Table of Contents
- [Introduction](#introduction)
- [Components](#components)
- [Software Installation](#software-installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project is designed to demonstrate how a camera can be used to track individuals or objects in motion. The servo allows for adjusting the camera's orientation.

## Components
- **Camera**: Used for capturing video feed.
- **Servo Motor**: Responsible for rotating the camera.
- **RPI**: Controls the camera and servo motor.
- External 5V power supply for the RPI
- Jumper wires
  
## Software Installation

1. **Prepare your Raspberry Pi**  
   Install Raspberry Pi OS (64‑bit recommended) and update:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install system dependencies
    ```bash
    sudo apt install python3 python3-pip python3-venv git opencv-data
    ```
3. Clone this repository
    ```bash
    git clone https://github.com/Sans-coding-the-skeleton/Person_Tracking_Camera_with_servo.git
    cd Person_Tracking_Camera_with_servo
    ```
4. Create a virtual environment and install Python packages
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
5. Run pigpio
    ```bash
    sudo pigpiod
    ```
## Usage
1. Connect the hardware components as described in the documentation.
2. Run the main script:
   ```bash
   python tracking.py
   ```

## Code Structure
- `tracking.py`: The main script for running the application.
- `calibration.py`: Contains the code for calibrating the servo motor if you use one different to MG90S.

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch and create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
