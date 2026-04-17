import streamlit as st
import numpy as np
import cv2
import mss
import time

from main_brain import detect_dark_patterns

st.set_page_config(layout="wide")

st.title("🛑 Dark Pattern AI")
st.subheader("Real-Time Computer Vision Detection")

start = st.button("Start Live Detection")

frame_placeholder = st.empty()
result_placeholder = st.empty()
alert_placeholder = st.empty()

if start:

    sct = mss.mss()

    while True:

        monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # -----------------------
        # Crop center (IMPORTANT)
        # -----------------------

        h, w, _ = frame.shape

        crop = frame[
            int(h*0.2):int(h*0.8),
            int(w*0.2):int(w*0.8)
        ]

        # Zoom
        crop = cv2.resize(crop, None, fx=1.5, fy=1.5)

        results = detect_dark_patterns(crop)

        frame_placeholder.image(
            crop,
            caption="Live Screen",
            use_container_width=True
        )

        result_placeholder.json(results)

        alert_placeholder.empty()

        if len(results["patterns"]) > 0:

            if results["risk_score"] > 60:
                alert_placeholder.error("⚠️ High Risk Dark Pattern")

            elif results["risk_score"] > 30:
                alert_placeholder.warning("⚠️ Medium Risk")

            else:
                alert_placeholder.info("⚠️ Low Risk")

        time.sleep(2)