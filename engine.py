import cv2
import numpy as np
import base64
import os

class ProctorEngine:
    def __init__(self):
        # Fallback to OpenCV Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Stabilization Buffer
        self.infraction_buffer_count = 0
        self.BUFFER_THRESHOLD = 9 # Require ~15-20 frames (approx 1 sec) to trigger alert, set to 9 for responsiveness

    def process_frame(self, base64_image):
        try:
            # Check if input is already a numpy array (Streamlit case)
            if isinstance(base64_image, np.ndarray):
                image = base64_image
            else:
                # Decode base64 image (Flask case)
                if ',' in base64_image:
                    base64_image = base64_image.split(',')[1]
                image_bytes = base64.b64decode(base64_image)
                np_arr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if image is None:
                return {'error': 'Failed to decode image'}

            # Convert to Grayscale for Haar Cascade
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Enhance contrast using histogram equalization to help in low light
            gray = cv2.equalizeHist(gray)
            
            # Detect faces with tuned parameters
            # minNeighbors reduced to 3 for better sensitivity
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
            
            face_count = len(faces)
            
            # --- STABILIZATION LOGIC ---
            current_frame_status = 'ok'
            if face_count > 1:
                current_frame_status = 'multiple_faces'
            elif face_count == 0:
                current_frame_status = 'no_face'
            
            is_infraction = False
            infraction_type = None

            if current_frame_status != 'ok':
                self.infraction_buffer_count += 1
                
                # Only trigger if we have seen this bad state for enough frames
                if self.infraction_buffer_count > self.BUFFER_THRESHOLD:
                    is_infraction = True
                    infraction_type = current_frame_status
            else:
                # Reset buffer immediately on good frame
                self.infraction_buffer_count = 0 
            
            return {
                'face_count': face_count,
                'is_infraction': is_infraction,
                'infraction_type': infraction_type
            }

        except Exception as e:
            print(f"Error in process_frame: {e}")
            return {'error': str(e)}
