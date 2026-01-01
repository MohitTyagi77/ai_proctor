import mediapipe as mp
try:
    print("mpl solutions dir:", dir(mp.solutions))
    import mediapipe.python.solutions.face_mesh
    print("Imported explicitly")
except Exception as e:
    print("Error:", e)
