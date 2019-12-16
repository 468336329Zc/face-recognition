import numpy as np

def face_distance_cos(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))


    return np.linalg.norm(face_encodings-face_to_compare,axis=1)
