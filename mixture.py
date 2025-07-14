import threading
import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import os
import webbrowser
import subprocess
import math
import screen_brightness_control as sbc
import pygetwindow as gw

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Recognizer for voice inpu`    +t
recognizer = sr.Recognizer()

# Screen and camera dimensions
screen_width, screen_height = pyautogui.size()
camera_width, camera_height = 640, 480

# Smoothing variables
prev_x, prev_y = 0, 0
smoothing_factor = 0.2

# Gesture states
left_click_held = False
left_click_triggered = False
right_click_triggered = False

# Helper function to calculate distance
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Virtual mouse function
# Updated Virtual Mouse Function with Scrolling
def virtual_mouse():
    global prev_x, prev_y, left_click_held, left_click_triggered, right_click_triggered
    cap = cv2.VideoCapture(0)
    global camera_width, camera_height
    camera_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    camera_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip and process frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark
                index_tip = landmarks[8]
                thumb_tip = landmarks[4]
                middle_tip = landmarks[12]

                # Map coordinates to screen space
                index_x, index_y = index_tip.x, index_tip.y
                screen_x = int(index_x * screen_width)
                screen_y = int(index_y * screen_height)
                smooth_x = prev_x + (screen_x - prev_x) * smoothing_factor
                smooth_y = prev_y + (screen_y - prev_y) * smoothing_factor
                prev_x, prev_y = smooth_x, smooth_y

                # Move cursor
                pyautogui.moveTo(smooth_x, smooth_y)

                # Gesture detection
                thumb_index_dist = calculate_distance(index_x, index_y, thumb_tip.x, thumb_tip.y)
                thumb_middle_dist = calculate_distance(middle_tip.x, middle_tip.y, thumb_tip.x, thumb_tip.y)
                index_middle_dist = calculate_distance(index_tip.x, index_tip.y, middle_tip.x, middle_tip.y)

                # Left-click gesture
                if thumb_index_dist < 0.05 and not left_click_triggered:
                    pyautogui.click()
                    left_click_triggered = True
                elif thumb_index_dist >= 0.05:
                    left_click_triggered = False

                # Left-click hold gesture
                if thumb_index_dist < 0.05 and not left_click_held:
                    pyautogui.mouseDown()
                    left_click_held = True
                elif thumb_index_dist >= 0.05 and left_click_held:
                    pyautogui.mouseUp()
                    left_click_held = False

                # Right-click gesture
                if thumb_middle_dist < 0.05 and not right_click_triggered:
                    pyautogui.rightClick()
                    right_click_triggered = True
                elif thumb_middle_dist >= 0.05:
                    right_click_triggered = False

                # Scroll gesture
                if index_middle_dist < 0.05:
                    pyautogui.scroll(-20)  # Scroll down
                elif index_middle_dist > 0.1:
                    pyautogui.scroll(20)  # Scroll up

        # Display feed
        cv2.putText(frame, "Press 'q' to Quit", (10, camera_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.imshow("Virtual Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Voice control function
def voice_control():
    while True:
        with sr.Microphone() as source:
            print("Listening for voice commands...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")

            if "exit" in text or "quit" in text:
                print("Exiting program...")
                break

            elif "increase volume" in text:
                pyautogui.press("volumeup", presses=5)
                print("Volume increased.")
            elif "decrease volume" in text:
                pyautogui.press("volumedown", presses=5)
                print("Volume decreased.")
            elif "mute" in text:
                pyautogui.press("volumemute")
                print("Muted.")

            elif "increase brightness" in text:
                brightness = sbc.get_brightness(display=0)
                new_brightness = min(brightness + 10, 100)
                sbc.set_brightness(new_brightness)
                print(f"Brightness increased to {new_brightness}%.")
            elif "decrease brightness" in text:
                brightness = sbc.get_brightness(display=0)
                new_brightness = max(brightness - 10, 0)
                sbc.set_brightness(new_brightness)
                print(f"Brightness decreased to {new_brightness}%.")

            elif "open google" in text:
                webbrowser.open("https://www.google.com")
                print("Google opened.")
            elif "search" in text:
                query = text.split("search for")[-1].strip()
                webbrowser.open(f"https://www.google.com/search?q={query}")
                print(f"Searching for: {query}")

        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print(f"Error with the service: {e}")

# Main function
def main():
    mouse_thread = threading.Thread(target=virtual_mouse, daemon=True)
    voice_thread = threading.Thread(target=voice_control, daemon=True)

    mouse_thread.start()
    voice_thread.start()

    mouse_thread.join()
    voice_thread.join()

if __name__ == "__main__":
    main()