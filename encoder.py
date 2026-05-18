
try:
    import numpy as np
    import face_recognition
    from pathlib import Path
    from typing import Optional
    from config import ENCODINGS_DIR,TOLERANCE,DETECTION_MODEL
except ModuleNotFoundError:
    print("Please install the requirements by using\npip install -r requirements.txt")

def computer_encondings(frames: list) -> list:
    """Take a list of numy frames and return it to extracted encondings """
    encodings = []
    for frame in frames:
        import cv2
        rgb = cv2.cvtColor(frame, cv2.COLOR_BAYER_BGR2RGB)
        
        locs = face_recognition.face_locations(rgb, model=DETECTION_MODEL)
        encs = face_recognition.face_encodings(rgb, locs)

        if encs:
            # If we have multiple faces we take the first one
            encodings.append(encs[0])
        return encodings
    

def save_usr(name: str, encodings: list) -> bool:
    """Save a profile of a user, Stock the average of every encodings
        (1Vector -> strongest one, reduct the false positif)"""
    if not encodings:
        return False
    #Average element per element
    mean_enc = np.mean(encodings, axis=0)
    path = ENCODINGS_DIR / f"{name}.npy"
    np.save(path, mean_enc)
    print(f"[Encoder] Profil {name} save in -> {path}")
    return True

def load_all_users() -> dict:
    "Load every users from ENCODINGS_DIR"
    "RETURN {name : encoding_array}"

    users = {}
    for npy_file in ENCODINGS_DIR.glob("*.npy"):
        name = npy_file.stem
        users[name] = np.load(npy_file)
    print(f"[Encoder] {len(users)} users loaded : {list(users.keys())}")
    return users

def del_users(name: str) -> bool:
    path = ENCODINGS_DIR / f"{name}.npy"
    if path.exists():
        path.unlink()
        return True
    return False


def recognize(encoding, saved_users: dict) -> tuple[str, float]:
    """Compare an anonymous encodings to every profiles saved"""
    if not saved_users:
        return "Unknonw", 1.0
    
    names = list(saved_users.keys())
    ref_encs = list(saved_users.values())
    distances = face_recognition.face_distance(ref_encs, encoding)
    best_idx = int(np.argmin(distances))
    best_dist = float(distances[best_idx])

    if best_dist < TOLERANCE:
        return names[best_idx], best_dist
    return "Unknown", best_dist
