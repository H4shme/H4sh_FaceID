import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

def frame_to_img(frame:np.ndarray, size:tuple | None = None) -> ImageTk.PhotoImage:
    """Convert OpenCV Frame to ImageTk.PhotoImage"""

    rgb = cv2.cvt(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    if size:
        img=img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image=img)

class VideoFrame(tk.Label):
    """
    vf=VideoFrame(parent, width=640, height=480)
    vf.pack()
    vf.update(frame)
    """

    def __init__(self, parent, width: int,height:int,**kwargs):
        super.__init__(parent,**kwargs)
        self._size=(width, height)
        #Black placehodler at launch
        self._show_black()
    def _show_black(self):
        black = np.zeros((*self.size[::-1], 3), dtype=np.uint8)
        self.update_frame(black)

    def update_frame(self, frame:np.ndarray):
        imgtk = frame_to_img(frame,self._size)

        self._imgtk = imgtk
        self.configure(image=imgtk)

class StatusBar(ttk.Label):
    def __init__(self,parent,**kwargs):
        self._var = tk.StringVar(value="")
        super().__init__(parent, textvariable=self._var, 
                         relief="sunken", anchor="w", padding=(10,4), 
                         **kwargs)
        
    def set(self, msg:str):
        self._var.set(msg)


class CountdownOverlay:
    @staticmethod
    def draw(frame: np.ndarray, value: int | str,
             color: tuple = (255, 255, 255)) -> np.ndarray:
        out = frame.copy()
        h, w = out.shape[:2]
        text = str(value)

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale=4.0
        thickness=6
        (tw,th), _ = cv2.getTextSize(text, font, scale, thickness)
        
        x = (w - tw)//2
        y = (h+th)//2

       # Shadow for the txt
        cv2.putText(out, text, (x + 3, y + 3), font, scale, (0, 0, 0), thickness + 2)
        cv2.putText(out, text, (x, y),          font, scale, color,     thickness)

        return out
   
class FaceBox:
    def draw(frame: np.ndarray,
             locations:list,
             names:list,
             distances:list) -> np.ndarray:
        out=frame.copy()

        for (top,right,bottom,left), name, dist in zip(locations, names, distances):
            color=FaceBox.COLOR_KNOWN if name!="Unknown" else FaceBox.COLOR_UNKNOWN

            cv2.rectangle(out,(left,top), (right,bottom), color,2)
            label = f"{name} ({dist:.2f})" if name != "Unknown" else name
            cv2.rectangle(out, (left,bottom), (right,bottom +26), color, cv2.FILLED)
            cv2.putText(out,label,(left+6, bottom +18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55,(255,255,255),1)
            

        return out
    
    
