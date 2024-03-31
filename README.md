# OMR-Scanner 📝🔍

This repository houses a versatile program crafted with OpenCV, C++, and Python, engineered to decipher OMR sheets and unveil the tally of correct responses post evaluation. The project boasts dual implementations: one in C++ for direct sheet processing and another in Python for both live feedback via webcam and analysis of pre-scanned images.

## Features 🌟

- **C++ Implementation**: Harnesses the power of image processing to discern filled markers on OMR sheets and computes scores against a predefined answer key. [🔗 C++ Implementation](https://github.com/D-Kumar19/OMR-Scanner/blob/master/OMR%20Scanner%20in%20CPP/Code/main.cpp)

- **Python Implementation**: Facilitates real-time checking through webcam feeds or the evaluation of stored scans, inclusive of answer key generation and score computation. [🔗 Python Implementation](https://github.com/D-Kumar19/OMR-Scanner/blob/master/OMR%20Scanner%20in%20Python/Source%20Code/main.py)

## Directory Structure 📂

- **OMR Scanner Project (C++)**: Hosts the C++ rendition of the project.
- **OMR Scanner in Python**: Contains the Python version of the project.
- **Images**: Designated storage for test images compatible with the Python implementation.
- **Result Images**: A repository for output images annotated with scores, exclusive to the Python version.

## Installation 💻

To embark on your journey with OMR-Scanner, clone the repository:

```bash
git clone https://github.com/<your-username>/OMR-Scanner.git
```

Ensure the installation of Python and OpenCV for Python's version, and the appropriate C++ compiler alongside OpenCV for C++'s rendition.

## Usage 🛠️

### C++ Implementation
- Navigate to the OMR Scanner Project directory.
- Compile the C++ program as directed in the project's README.
- Execute the program, which encompasses:
  - Capturing a bird's eye view of the OMR sheet.
  - Identifying contours and filled boxes.
  - Highlighting correct answers via image processing techniques.
  - Comparing detected answers with the answer key.
  - Outputting the score and accuracy in the terminal.

### Python Implementation
- In the OMR Scanner in Python directory, execute the Python script.
- Opt between live checking with a webcam or the evaluation of stored images, involving:
  - Generation of an answer key from a solution image.
  - Analysis of question images for comparison.
  - Identification of filled markers by dissecting the image into rows and columns.
  - Storage of annotated result images in the main directory.

## Contributing 🤝
Eager to enhance OMR-Scanner? We warmly welcome your contributions! Should you have innovative ideas or improvements, follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b <branch_name>`).
3. Commit your changes (`git commit -m 'Added some features...'`).
4. Push to the branch (`git push origin <branch_name>`).
5. Open a pull request.
