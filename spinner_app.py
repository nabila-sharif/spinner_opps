import streamlit as st
import math
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

class WheelSpinner:
    def __init__(self):
        self.angle = 0
        self.running = False
        self.selected_index = None
        self.center = (200, 200)
        self.radius = 140
        self.segments = 6
        self.base_colors = ["#b3e5fc", "#81d4fa", "#4fc3f7", "#29b6f6", "#03a9f4", "#039be5"]

    def draw_wheel(self, placeholder):
        fig, ax = plt.subplots(figsize=(6, 6))
        angle = self.angle
        selected = self.selected_index

        for i in range(self.segments):
            start_angle = (360 / self.segments) * i + angle
            extent = 360 / self.segments
            color = "yellow" if selected is not None and i == selected else self.base_colors[i % len(self.base_colors)]
            wedge = Wedge(self.center, self.radius, start_angle, start_angle + extent, color=color, ec="white", lw=2)
            ax.add_patch(wedge)

            mid_angle = math.radians(start_angle + extent / 2)
            x = self.center[0] + (self.radius / 1.7) * math.cos(mid_angle)
            y = self.center[1] + (self.radius / 1.7) * math.sin(mid_angle)
            ax.text(x, y, str(i + 1), ha='center', va='center', fontweight='bold', fontsize=16, color="black")

        ax.plot([200, 200], [20, 40], color="orange", lw=3)
        ax.plot([200, 190], [40, 30], color="orange", lw=3)
        ax.plot([200, 210], [40, 30], color="orange", lw=3)

        if selected is not None:
            ax.text(200, 200, str(selected + 1), ha='center', va='center', fontweight='bold', fontsize=40, color="red")

        ax.set_aspect('equal')
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 400)
        ax.axis('off')
        placeholder.pyplot(fig)

    def spin(self, placeholder):
        if not self.running:
            self.running = True
        speed = 15
        deceleration = 0.05

        while self.running and speed > 0:
            self.angle = (self.angle + speed) % 360
            self.draw_wheel(placeholder)
            time.sleep(0.05)
            speed = max(0, speed - deceleration)

        if not self.running:
            return  # stopped manually, result handled in stop_spin()

        self.running = False
        self.show_result(placeholder)

    def stop_spin(self, placeholder):
        self.running = False
        self.show_result(placeholder)

    def show_result(self, placeholder):
        final_angle = (360 - self.angle) % 360
        segment_angle = 360 / self.segments
        self.selected_index = int(final_angle // segment_angle)
        selected_number = self.selected_index + 1
        self.draw_wheel(placeholder)
        st.success(f"🎯 Selected Number: {selected_number}")


# Page setup
st.set_page_config(page_title="Wheel Spinner", layout="centered")
st.title("🎡 Manual Stop Wheel Spinner")

# Button styling
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        padding: 15px 0;
        font-size: 18px;
        border-radius: 10px;
        width: 100%;
    }
    div.stButton:nth-child(2) > button {
        background-color: #f44336 !important;
        color: white;
        padding: 15px 0;
        font-size: 18px;
        border-radius: 10px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Session state for spinner instance and control
if "spinner" not in st.session_state:
    st.session_state.spinner = WheelSpinner()

wheel = st.session_state.spinner
placeholder = st.empty()

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start"):
        wheel.selected_index = None
        wheel.running = True
        wheel.spin(placeholder)

with col2:
    if st.button("Stop"):
        wheel.stop_spin(placeholder)

# Always draw latest state
if not wheel.running:
    wheel.draw_wheel(placeholder)
