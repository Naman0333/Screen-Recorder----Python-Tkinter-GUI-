import tkinter as tk
import cv2
import numpy as np
import pyautogui
import threading

class ScreenRecorder:
    def __init__(self,window):
        
        # Initialize the ScreenRecorder object with a master Tkinter window
        self.window = window
        window.wm_title('Screen Recorder')

        # Create a Headline to display to the user    
        self.label = tk.Label(window, text="Screen Recorder", font=("Arial",30,"bold"), bg="black", fg="white")
        self.label.pack(fill="x",pady=5)
        
        # Create a 'Record' button that starts the recording process when clicked
        self.button_frame = tk.Frame(window)
        self.button_frame.pack()

        # Create a 'Rec ord' button that starts the recording process when clicked
        self.record_button = tk.Button(self.button_frame, text="Record", width=16, font=("Arial",10 ,"bold"), command=self.start_recording)
        self.record_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create a 'Stop' button that stop the recording process when clicked.
        self.stop_button = tk.Button(self.button_frame, text="Stop", width=16, font=("Arial",10,"bold"), command=self.stop_recording)
        self.stop_button.pack(side=tk.LEFT, padx=20, pady=10)
         
        # Create a 'Quit' button that exits the application when clicked.
        self.quit_button = tk.Button(self.button_frame, text="Quit", width=16, font=("Arial",10,"bold"),command=window.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Set the screen size to the full resolution of the primary moniter
        self.SCREEN_SIZE = (1920, 1080)

        # Set the video codec to MJPG
        self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")

        # Initialize the output video file to None
        self.out = None

        # Initialize the is_recording flag to false
        self.is_recording = None



    def start_recording(self):

        # Change the label text to indicate the recording is in process.
        self.label.config(text = "Recording...")

        # Disable the 'Record' button and enable the 'Stop' Button.
        self.record_button.config(state= tk.DISABLED)
        self.stop_button.config(state = tk.NORMAL)

        # Create a new VideoWriter object to start writing frames to the output file
        self.out = cv2.VideoWriter('output.avi', self.fourcc, 20.0, self.SCREEN_SIZE)
        
        # Set the is_recording flat to True
        self.is_recording =True

        # Start a new thread to continuosly capture the write frames to the output file.
        self.recording_thread = threading.Thread(target=self.record_loop)
        self.recording_thread.start()

    def record_loop(self):
        # Continuously capture and write frames to the output file until recording is stopped
        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(frame)    
            
        # Release the output video file recording is stopped
        self.out.release()

        # Change the label text and button states back to their initial values
        self.label.config(text = "Press 'Record' to start Recording")
        self.record_button.config(state= tk.NORMAL)
        self.stop_button.config(state = tk.DISABLED)


    def stop_recording(self):
        # Set the is_processing flag to False to stop the recording loop.
        self.is_recording = False

# Create a new Tkinter window and initialze a ScreenRecorder object.
root = tk.Tk()
screen_recorder = ScreenRecorder(root)

# Set the size of the window to 800x600 pixels and icon of app.
root.geometry('800x600')
root.iconbitmap('icon.ico')

# Start the main event loop to display the window and respond to user input
root.mainloop()
