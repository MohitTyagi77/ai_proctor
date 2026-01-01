import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import av
import numpy as np
from engine import ProctorEngine
import time

# --- Setup Page ---
st.set_page_config(page_title="AI Proctoring System", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #171717 100%);
        color: #f8fafc;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        background: linear-gradient(to right, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.4);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("AI Proctoring System")

# --- Initialize Engine (Cached) ---
@st.cache_resource
def get_engine():
    return ProctorEngine()

if 'trust_score' not in st.session_state:
    st.session_state['trust_score'] = 100.0

if 'log' not in st.session_state:
    st.session_state['log'] = []

# --- Video Processor ---
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.engine = get_engine()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Process frame
        # We need to access the engine safely
        # Note: Session state is not thread-safe inside webrtc callback easily.
        # So we might re-instantiate or just use global if needed, 
        # but here we passed reference.
        
        result = self.engine.process_frame(img)
        
        # Draw on frame (HUD style) because updating Streamlit UI from here is hard
        
        # 1. Valid Face
        face_count = result.get('face_count', 0)
        is_infraction = result.get('is_infraction', False)
        infraction_type = result.get('infraction_type')
        
        # Status Text
        status_text = f"Faces: {face_count}"
        color = (0, 255, 0) # Green
        
        if is_infraction:
            color = (0, 0, 255) # Red
            if infraction_type == 'no_face':
                 status_text = "NO FACE DETECTED!"
            elif infraction_type == 'multiple_faces':
                 status_text = "MULTIPLE FACES!"
        
        # Overlay Status
        cv2.putText(img, status_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Trust Score Overlay (Simplified for Streamlit)
        # We can't easily sync back to main thread trust_score variable without a queue.
        # For simplicity in this demo, we just show "Monitoring..." on video.
        cv2.putText(img, "Monitoring Active", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Camera Feed")
    webrtc_streamer(
        key="proctor-feed",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

with col2:
    st.markdown("### Proctoring Status")
    
    # Placeholder metrics (Note: Real-time update in Streamlit from Webrtc is complex)
    # Most Streamlit Webrtc apps do visualization ON the video stream (as done above)
    # or use a queue to pass data back.
    
    st.info("The Trust Score logic runs in the background. Please check the video feed for real-time status overlays.")
    
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Allow camera access.")
    st.markdown("2. Ensure your face is clearly visible.")
    st.markdown("3. Avoid lookinig away or having multiple people in frame.")
