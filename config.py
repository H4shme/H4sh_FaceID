from pathlib import Path


# Paths

ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
ENCODINGS_DIR = DATA_DIR / 'encodings'
ENCODINGS_DIR.mkdir(parents=True, exist_ok=True)

# Cam resolution

CAM_INDEX = 0
CAM_WIDTH = 640
CAM_HEIGHT = 480

# Tolerance in resolution
# 0.4 = Strict | 0.5 = mid | 0.6 = permissible
TOLERANCE = 0.5


# Detection model (hog = fast cpu | "cnn" = hard gpu)
DETECTION_MODEL = "hog"

# Init phase

ENROLL_SHOTS = 5 # Automatic shots during initialization
ENROLL_DELAY_MS = 600 #Delay between shots 
ENROLL_COUNTDOWN = 3 #Delay bfr first shot

# Window
APP_TITLE = "H4sh FaceID"
WIN_WIDTH = 700
WIN_HEIGHT = 560
FPS_TARGET = 30
