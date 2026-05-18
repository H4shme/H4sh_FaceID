import cv2
import numpy as np
from config import CAM_INDEX, CAM_HEIGHT, CAM_WIDTH

class Camera:
    """Wrapp around cv2.VideoCapture
        Use like context manager
        
        with Camera() as cam:
            frame = cam.read()"""
    
    def __init__(self, index: int=CAM_INDEX):
        self._cap = None
        self._index = index

    def open(self):
        """Open video and config the resolution"""
        self._cap = cv2.VideoCapture(self._index)

        if not self._cap.isOpened():
            raise RuntimeError(f"Impossilbe d'ouvrir la caméra (index={self._index})")
        # Force the resolution in camera.py
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

        print(f"[Camera] Open : {int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x"
              f'{int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}')
        

    def read(self) -> np.ndarray | None: # Frame or None 
        "Read current frame return BGR numpy array or None"
        if self._cap is None:
            return None
        ret, frame = self._cap.read()
        return frame if ret else None # We return the frame if ret==True
    def read_flipped(self) -> np.ndarray | None:
        "Read frame and turn it horizontaly (mirror effect)"
        frame = self.read()
        if frame is None: 
            return None
        return cv2.flip(frame,1) # 1= horizontaly flip
    def close(self):
        if self._cap and self._cap.isOpened():
            self._cap.release()
            self._cap = None
            print("[Camera] Closed")

    def __enter__(self):
        self.open()
        return self
    def __exit__(self, *_):
        self.close()
