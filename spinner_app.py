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
            # Highlight the selected segment in yellow
            color = "yellow" if selected is not None and i == selected else self.base_colors[i % len(self.base_colors)]
            wedge = Wedge(self.center, self.radius, start_angle, start_angle + extent, color=color, ec="white", lw=2)
            ax.add_patch(wedge)

            # Number label
            mid_angle = math.radians(start_angle + extent / 2)
            x = self.center[0] + (self.radius / 1.7) * math.cos(mid_angle)
            y = self.center[1] + (self.radius / 1.7) * math.sin(mid_angle)
            ax.text(x, y, str(i + 1), ha='center', va='center', fontweight='bold', fontsize=16, color="black")

        # Pointer
        ax.plot([200, 200], [20, 40], color="orange", lw=3)
        ax.plot([200, 190], [40, 30], color="orange", lw=3)
        ax.plot([200, 210], [40, 30], color="orange", lw=3)

        # Selected number in center
        if selected is not None:
            ax.text(200, 200, str(selected + 1), ha='center', va='center', fontweight='bold', fontsize=40, color="red")

        ax.set_aspect('equal')
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 400)
        ax.axis('off')
        placeholder.pyplot(fig)

    def start_spin(self, placeholder):
        if not self.running:
            self.running = True
            self.selected_index = None
            speed = 15
            deceleration = 0.1
            max_spin_time = 5
            start_time = time.time()

            while self.running and (time.time() - start_time < max_spin_time):
                self.angle = (self.angle + speed) % 360
                self.draw_wheel(placeholder)
                time.sleep(0.05)
                speed = max(1, speed - deceleration)

            self.running = False
            final_angle = (360 - self.angle) % 360
            segment_angle = 360 / self.segments
            self.selected_index = int(final_angle // segment_angle)
            selected_number = self.selected_index + 1
            self.draw_wheel(placeholder)
            st.success(f"🎯 Selected Number: {selected_number}")

    def stop_spin(self):
        self.running = False


# Streamlit UI
st.set_page_config(page_title="Wheel Spinner", layout="centered")
st.title("🎡 Wheel Spinner")

# CSS for button colors
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

# Instantiate wheel
wheel = WheelSpinner()
placeholder = st.empty()

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start"):
        wheel.start_spin(placeholder)
with col2:
    if st.button("Stop"):
        wheel.stop_spin()

# Initial render
wheel.draw_wheel(placeholder)
