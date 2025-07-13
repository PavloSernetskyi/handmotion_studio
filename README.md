# HandMotion Studio

HandMotion Studio is an interactive AR/VR desktop application built with Python and OpenCV that enables real-time hand gesture-based interaction with virtual games and objects using a webcam. The current version includes a **Ping Pong game** and a **Playground mode** featuring 3D objects like a cube, basketball, and beer can.

---
##  Screenshots

>  Screenshots of gameplay and gesture controls to show off project visually:


---
##  Folder Structure

```
handmotion_studio/
├── assets/                  # Game assets (beer, basketball, cube, paddle images)
│   ├── beer_can.png
│   ├── basketball.png
│   ├── cube.png
│   └── paddle.png
├── games/                   # Individual games live here
│   └── pingpong.py          # Ping Pong game logic
├── .gitignore
├── app.py                   # Main app entry point (UI, menu, gesture routing)
├── gesture_recognizer.py    # Gesture classification (grab, pinch, open)
├── hand_tracker.py          # Hand landmark detection (using MediaPipe)
├── objects.py               # VirtualObject class for draggable objects
├── requirements.txt         # Python dependencies
├── test_image_load.py       # Utility to test asset loading
└── README.md                # Project documentation
```

---

## Features

- 🖐️ Real-time hand tracking using MediaPipe
-  Gesture-based controls:
  - **Pinch** to navigate menus and exit games
  - **Grab/Open** to pick up and release objects
-  **Ping Pong Game** with AI paddle and ball physics
-  **Playground Mode** with draggable cube, basketball, and beer
-  VirtualObject abstraction for easy object handling and future game expansions
-  Modular structure for easily adding more games like Air Hockey, etc.
-  AI opponent paddle behavior in Ping Pong

---

##  Technologies Used

| Tech              | Purpose                              |
|-------------------|--------------------------------------|
| **Python 3.10+**   | Main programming language            |
| **OpenCV**         | Real-time video capture & rendering  |
| **MediaPipe**      | Hand landmark detection              |
| **NumPy**          | Array operations (indirect via OpenCV)|
| **OOP**            | Game logic and virtual object structure |
| **Modular Python** | Maintainable folder & file structure |

---

##  Setup Instructions

### 1.  Clone the repository

```bash
git clone https://github.com/your-username/handmotion_studio.git
cd handmotion_studio
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, manually install the following:

```bash
pip install opencv-python mediapipe numpy
```

---

##  How to Run

Make sure your webcam is connected, then run:

```bash
python app.py
```
---

##  Skills Demonstrated

-  Computer Vision with OpenCV
-  Real-time hand tracking (MediaPipe)
-  Game development concepts (collisions, AI opponent)
-  Modular software architecture in Python
-  Gesture recognition and input control
-  Object-oriented design for reusable logic
-  Refactoring and scalable code structuring

---

## Author

**Pavlo Sernetskyi**  
A creative developer passionate about blending **AR/VR**, **AI**, and **interactive gaming** experiences.

---
