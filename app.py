import wmi
import speech_recognition as sr
import os
import webbrowser
import subprocess
import pyautogui  # For automating tasks like volume
import screen_brightness_control as sbc  # For brightness control

recognizer = sr.Recognizer()

def capture_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text

def process_voice_command(text):
    text = text.lower()

    # Greeting and Goodbye
    if "hello" in text:
        print("Hello! How can I help you?")
    elif "goodbye" in text or "exit" in text:
        print("Goodbye! Have a great day!")
        return True

    # System control commands
    elif "shut down" in text:
        print("Shutting down the computer...")
        os.system("shutdown /s /t 1")
    elif "restart" in text:
        print("Restarting the computer...")
        os.system("shutdown /r /t 1")
    elif "lock the screen" in text:
        print("Locking the screen...")
        os.system("rundll32.exe user32.dll, LockWorkStation")
    
    # Volume Control
    elif "increase volume" in text:
        pyautogui.press("volumeup", presses=5)
        print("Increasing volume...")
    elif "decrease volume" in text:
        pyautogui.press("volumedown", presses=5)
        print("Decreasing volume...")
    elif "mute" in text:
        pyautogui.press("volumemute")
        print("Muting the sound...")
    elif "unmute" in text:
        pyautogui.press("volumemute")  # Pressing "mute" key again unmutes if it's currently muted
        print("Unmuting the sound...")

    # Brightness control using screen_brightness_control library
    elif "increase brightness" in text:
        current_brightness = sbc.get_brightness(display=0)  # Get brightness of the first display
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]  # Handle multiple monitors if necessary
        new_brightness = min(current_brightness + 10, 100)  # Cap brightness at 100%
        sbc.set_brightness(new_brightness)
        print(f"Increasing brightness to {new_brightness}%")
    elif "decrease brightness" in text:
        current_brightness = sbc.get_brightness(display=0)  # Get brightness of the first display
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]  # Handle multiple monitors if necessary
        new_brightness = max(current_brightness - 10, 0)  # Do not go below 0%
        sbc.set_brightness(new_brightness)
        print(f"Decreasing brightness to {new_brightness}%")
    
    # File Management
    elif "open documents" in text:
        print("Opening Documents folder...")
        os.startfile(r'C:/Users/kashishpreet kaur/OneDrive/Desktop/Documents')  # Change path accordingly
    elif "create folder" in text:
        folder_name = text.split("create folder")[-1].strip()
        os.makedirs(os.path.join(os.getcwd(), folder_name))
        print(f"Created folder '{folder_name}'")
    elif "open file" in text:
        file_path = text.split("open file")[-1].strip()
        try:
            os.startfile(file_path)
            print(f"Opening file '{file_path}'")
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Please provide a valid path.")

    # Web Browsing
    elif "open google" in text:
        print("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "search" in text:
        query = text.split("search for")[-1].strip()
        print(f"Searching for {query}...")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # Application Control
    elif "open word" in text:
        print("Opening Microsoft Word...")
        os.startfile(r'C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE')  # Change path as per your installation
    elif "open chrome" in text:
        print("Opening Google Chrome...")
        os.startfile(r'C:/Program Files/Google/Chrome/Application/chrome.exe')
    elif "open excel" in text:
        print("Opening Microsoft Excel...")
        os.startfile(r'C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE')  # Change path as per your installation

    # Handle unrecognized commands
    else:
        print("I didn't understand that command. Please try again.")
    
    return False

def main():
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)

if __name__ == "__main__":
    main()








# import speech_recognition as sr
# from gtts import gTTS
# import winsound
# from pydub import AudioSegment
# import pyautogui
# import webbrowser
# import os

# def listen_for_command():
#     recognizer = sr.Recognizer()

#     with sr.Microphone() as source:
#         print("Listening for commands...")
#         recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusts based on ambient noise
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio)
#         print("You said:", command)
#         return command.lower()
#     except sr.UnknownValueError:
#         print("Could not understand audio. Please try again.")
#         return None
#     except sr.RequestError:
#         print("Unable to access the Google Speech Recognition API.")
#         return None

# def respond(response_text):
#     print(response_text)
#     tts = gTTS(text=response_text, lang='en')
#     tts.save("response.mp3")
#     sound = AudioSegment.from_mp3("response.mp3")
#     sound.export("response.wav", format="wav")
#     winsound.PlaySound("response.wav", winsound.SND_FILENAME)
#     cleanup_audio_files()

# def cleanup_audio_files():
#     if os.path.exists("response.mp3"):
#         os.remove("response.mp3")
#     if os.path.exists("response.wav"):
#         os.remove("response.wav")

# tasks = []
# listeningToTask = False

# def main():
#     global tasks
#     global listeningToTask
#     while True:
#         command = listen_for_command()

#         triggerKeyword = "bologna"

#         if command and triggerKeyword in command:
#             if listeningToTask:
#                 tasks.append(command)
#                 listeningToTask = False
#                 respond(f"Added '{command}' to your task list. You have {len(tasks)} tasks.")
#             elif "add a task" in command:
#                 listeningToTask = True
#                 respond("Sure, what is the task?")
#             elif "list tasks" in command:
#                 if tasks:
#                     task_list = "Your tasks are: " + ", ".join(tasks)
#                     respond(task_list)
#                 else:
#                     respond("Your task list is currently empty.")
#             elif "take a screenshot" in command:
#                 pyautogui.screenshot("screenshot.png")
#                 respond("I took a screenshot for you.")
#             elif "open chrome" in command:
#                 respond("Opening Chrome.")
#                 webbrowser.open("http://www.youtube.com/@JakeEh")
#             elif "exit" in command:
#                 respond("Are you sure you want to exit?")
#                 confirmation = listen_for_command()
#                 if "yes" in confirmation:
#                     respond("Goodbye!")
#                     break
#                 else:
#                     respond("Okay, continuing...")
#             else:
#                 respond("Sorry, I'm not sure how to handle that command.")

# if __name__ == "__main__":
#     main()


# # import speech_recognition as sr
# # from gtts import gTTS
# # import winsound
# # from pydub import AudioSegment
# # import pyautogui
# # import webbrowser

# # def listen_for_command():
# #     recognizer = sr.Recognizer()

# #     with sr.Microphone() as source:
# #         print("Listening for commands...")
# #         recognizer.adjust_for_ambient_noise(source)
# #         audio = recognizer.listen(source)

# #     try:
# #         command = recognizer.recognize_google(audio)
# #         print("You said:", command)
# #         return command.lower()
# #     except sr.UnknownValueError:
# #         print("Could not understand audio. Please try again.")
# #         return None
# #     except sr.RequestError:
# #         print("Unable to access the Google Speech Recognition API.")
# #         return None

# # def respond(response_text):
# #     print(response_text)
# #     tts = gTTS(text=response_text, lang='en')
# #     tts.save("response.mp3")
# #     sound = AudioSegment.from_mp3("response.mp3")
# #     sound.export("response.wav", format="wav")
# #     winsound.PlaySound("response.wav", winsound.SND_FILENAME)
# #     # os.system("afplay response.mp3") for non-windows

# # tasks = []
# # listeningToTask = False

# # def main():
# #     global tasks
# #     global listeningToTask
# #     # respond("Hello, Jake. I hope you're having a nice day today.")
# #     while True:
# #         command = listen_for_command()

# #         triggerKeyword = "bologna"

# #         if command and triggerKeyword in command:
# #             if listeningToTask:
# #                 tasks.append(command)
# #                 listeningToTask = False
# #                 respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
# #             elif "add a task" in command:
# #                 listeningToTask = True
# #                 respond("Sure, what is the task?")
# #             elif "list tasks" in command:
# #                 respond("Sure. Your tasks are:")
# #                 for task in tasks:
# #                     respond(task)
# #             elif "take a screenshot" in command:
# #                 pyautogui.screenshot("screenshot.png")
# #                 respond("I took a screenshot for you.")
# #             elif "open chrome" in command:
# #                 respond("Opening Chrome.")
# #                 webbrowser.open("http://www.youtube.com/@JakeEh")
# #             elif "exit" in command:
# #                 respond("Goodbye!")
# #                 break
# #             else:
# #                 respond("Sorry, I'm not sure how to handle that command.")

# # if __name__ == "__main__":
# #     print(listen_for_command())
# #     # respond("This has been building a virtual assistant with Python")
# #     main()