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
        pass # Faut j'me tire j'reprends après
