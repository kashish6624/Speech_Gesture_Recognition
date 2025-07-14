# Speech and Gesture Recognition System

This project integrates **speech recognition** and **hand gesture detection** to create a seamless and hands-free system control experience. It allows users to perform tasks like media control, brightness adjustment, volume control, cursor movement, and web browsing using **voice commands** and **hand gestures**.

---

## Project Files

### `merge.py`
A complete integration of gesture recognition and voice command handling.

- Voice Commands:
  - Shutdown, restart, lock screen
  - Open applications (Chrome, Word, Excel)
  - Control brightness and volume
  - Web search and site opening
- Gesture Controls:
  - Adjust volume by distance between fingers
  - Play/Pause and Skip media with hand gestures
  - Recognizes left and right hand for different actions

---

### `mixture.py`
Multithreaded implementation for running virtual mouse and voice control in parallel.

- 🖱️ Virtual Mouse:
  - Cursor movement via index finger
  - Click, hold, right-click, and scroll gestures
- 🎤 Voice Control:
  - Adjust volume and brightness
  - Open websites and perform searches
  - Exit via voice command

---

### `speechReco.py`
A lightweight standalone script focused on **speech-only** interaction.

- Recognizes current active window
- Supports:
  - Media playback (play/pause, skip)
  - System controls
  - File operations (open folders, files, create folder)
  - Web and application control

### `virtualMouse.py`
Gesture-only real-time system that:
- Controls mouse cursor using **index finger**
- Detects **clicks**, **play/pause**, and **media skips** based on thumb-index distance
- Supports hand side detection (Left = back, Right = forward)
- Optionally opens a folder on click
> Uses **MediaPipe** and **OpenCV** for hand tracking.

---

### `app.py`
Standalone lightweight voice assistant for:
-  **Volume & Brightness control**
-  **System commands**: shutdown, restart, lock
-  **File system actions**: open folders, create/open files
-  **Web search** and **app launching**
> Designed for smooth spoken command-based automation.
---

## 🛠️ Technologies Used

- **Python**
- **Libraries**:
  - `OpenCV` – Video capture and frame processing
  - `MediaPipe` – Hand landmark detection
  - `SpeechRecognition`, `PyAudio` – Voice input
  - `pyautogui` – Mouse/keyboard automation
  - `screen_brightness_control` – Brightness adjustment
  - `pygetwindow` – Active window detection
  - `threading`, `wmi`, `os`, `webbrowser`, `subprocess`
