import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import face_recognition
from config import(CAM_WIDTH, CAM_HEIGHT,ENROLL_SHOTS,
                   ENROLL_DELAY_MS,ENROLL_COUNTDOWN,
                   DETECTION_MODEL,FPS_TARGET)
from camera import Camera
from encoder import computer_encondings, save_usr, recognize
from widgets import VideoFrame, StatusBar, CountdownOverlay, FaceBox


class EnrollView(tk.Frame):
    """Initializion phase 
    User enter name, look the camera and sys capture n photos 
    to create his profile
    
    Cycle : 
    IDLE -> Start -> Countdown -> Capturing -> Done"""

    def __init__(self,parent,camera:Camera,on_done:callable):
        super().__init__(parent)
        self._cam=camera
        self._done=on_done # callback. called when enrollement is finished
        

        self._state = "IDLE"
        self._countdown = ENROLL_COUNTDOWN
        self._shotsleft = ENROLL_SHOTS
        self._captured_frames = [] # raw frames accumulated for encoding
        self._after_id = None

        self._build_ui()
        self._tick()

    def _build_ui(self):
        ttk.Label(self, text="Create a new profile",
                  font=("Helvetica", 16, "bold")).pack(pady=(16,4))
        ttk.Label(self, text="Enter your name and look at the camera",
                  foreground="gray").pack(pady=(0,12))
        


        name_frame=ttk.Frame(self)
        name_frame.pack()
        ttk.Label(name_frame, text="Name : ").pack(side="left", padx=(0,8))
        self._name_var=tk.StringVar()
        self._name_entry=ttk.Entry(name_frame, textvariable=self._name_var, width=22)
        self._name_entry.pack(side="left")

        # Video 
        self._video=VideoFrame(self, CAM_WIDTH//2,CAM_HEIGHT//2)
        self._video.pack(pady=12)

                


