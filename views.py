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

        # Progress Bar
        self._progress = ttk.Progressbar(self, lenght=320,
                                         maximum=ENROLL_SHOTS, mode="determinate")
        self._progress.pack(pady=(0,8))

        # Start Button
        self._btn=ttk.Button(self, text="📸 Start Capturing",
                             command=self.start_enrollment)
        self._btn.pack(pady=(0,8))

        #Status bar 
        self._status=StatusBar(self)
        self._status.pack(fill='x', side="bottom")
        self._status.set('Enter you name then click on Start')


    def _tick(self):
        """Video loop : read the cam and update the display"""
        frame = self._cam.read_flipped()
        if frame is not None:
            display=frame
            if self._state=='COUNTDOWN':
                display = CountdownOverlay.draw(frame, self._countdown, (0,220,255))
            elif self._state=='CAPTURING':
                display=CountdownOverlay.draw(frame, "📸", (50,200,50))
                self._captured_frames.append(frame.copy())
                self._shotsleft-=1
                self._progress["value"] = ENROLL_SHOTS - self._shotsleft
                self._status.set(f"Captures {ENROLL_SHOTS - self._shotsleft}/{ENROLL_SHOTS}")

                if self._shotsleft<=0:
                    self._state='PROCESSING'
                    self.process_enrollment()
                    return
                else:
                    self.state='WAIT_NEXT'
            self._video.update_frame(display)
        ms =ENROLL_DELAY_MS if self._state=="WAIT_NEXT"else 1000 //FPS_TARGET
        if self._state=='WAIT_NEXT':
            self._state='CAPTURING'
        self._after_id=self.after(ms, self._tick)
    def _start_enrollment(self):
        name = self._name_var.get().strip()
        if not name:
            messagebox.showwarning("Name missing", "Please enter a name")
            return
        self._btn.state(["disabled"])
        self._name_entry.state(["disabled"])
        self._captured_frames.clear()
        self._shotsleft=ENROLL_SHOTS
        self._progress["value"] = 0
        self._countdown =ENROLL_COUNTDOWN
        self._state='COUNTDOWN'
        self._run_countdown()

    def _run_countdown(self):
        """Countdown bfr first shot"""

        if self._countdown>0:
            self._status.set(f"Prepare yourseulf... {self._countdown}")
            self._countdown -=1
            self.after(1000, self._run_countdown)
        else:
            self._state="CAPTURING"
    
    def _process_enrollment(self):
        self._status.set("Encodings calculation in progress...")
        name=self._name_var.get().strip()

        encodings= computer_encondings(self._captured_frames)

        if not encodings:
            messagebox.showerror("Error", "No face detected in the shots\nRetry")
            self._reset()
            return
        ok =save_usr(name, encodings)
        if ok:
            self._status.set(f"Profil '{name}' created with {len(encodings)} encodings.")
            self._after(1200, self._on_done)
        else:
            messagebox.showerror('Error', 'Unable to save the profile')
            self._reset()
        
    def _reset(self):
        self._state='IDLE'
        self._btn_state(["!disabled"])
        self._name_entry.state(["!disabled"])
        self._progress["value"] = 0
        self._status.set("Enter you name then click on Start.")


    def destroy(self):
        if self._after_id:
            self.after_cancel(self._after_id)
        
        super().destroy()

class RecognizeView(tk.Frame):
    pass
