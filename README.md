# Speech and Gesture Recognition System

This project integrates **speech recognition** and **hand gesture detection** to create a seamless and hands-free system control experience. It allows users to perform tasks like media control, brightness adjustment, volume control, cursor movement, and web browsing using **voice commands** and **hand gestures**.

---

## Project File

### `speechReco.py`
A lightweight standalone script focused on **speech-only** interaction.

- Recognizes current active window
- Supports:
  - Media playback (play/pause, skip)
  - System controls
  - File operations (open folders, files, create folder)
  - Web and application control
---
## Technology used
  - `SpeechRecognition` – Voice input
  - `pyautogui` – Mouse/keyboard automation
  - `screen_brightness_control` – Brightness adjustment
  - `pygetwindow` – Active window detection
  - `wmi`, `os`, `webbrowser`, `subprocess`
