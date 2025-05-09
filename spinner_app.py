import streamlit as st
import math
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

# Spinner base class
class Spinner:
    def __init__(self, segments, radius, center):
        self.angle = 0
        self.selected_index = None
        self.center = center
        self.radius = radius
        self.segments = segments

    def draw(self, placeholder):
        pass

    def spin_once(self, placeholder):
        pass

# Derived class for wheel spinner
class WheelSpinner(Spinner):
    def __init__(self, segments=6):
        super().__init__(segments=segments, radius=140, center=(200, 200))
        self.base_colors = ["#b3e5fc", "#81d4fa", "#4fc3f7", "#29b6f6", "#03a9f4", "#039be5"]
        self.speed = 0

    def draw(self, placeholder):
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

        # Draw pointer dynamically
        cx, cy = self.center
        ax.plot([cx, cx], [cy - self.radius - 20, cy - self.radius], color="orange", lw=3)
        ax.plot([cx, cx - 10], [cy - self.radius, cy - self.radius + 10], color="orange", lw=3)
        ax.plot([cx, cx + 10], [cy - self.radius, cy - self.radius + 10], color="orange", lw=3)

        if selected is not None:
            ax.text(cx, cy, str(selected + 1), ha='center', va='center', fontweight='bold', fontsize=40, color="red")

        ax.set_aspect('equal')
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 400)
        ax.axis('off')
        placeholder.pyplot(fig)

    def spin_and_animate(self, placeholder):
        self.selected_index = None
        self.speed = 10
        total_frames = 60
        slowdown_rate = 0.95

        for _ in range(total_frames):
            if not st.session_state.running:
                break
            self.angle = (self.angle + self.speed) % 360
            self.speed *= slowdown_rate
            self.draw(placeholder)
            time.sleep(0.05)

        st.session_state.running = False
        self.select_segment(placeholder)

    def select_segment(self, placeholder):
        final_angle = (360 - self.angle) % 360
        segment_angle = 360 / self.segments
        self.selected_index = int(final_angle // segment_angle)
        self.draw(placeholder)
        st.success(f"🎯 Selected Number: {self.selected_index + 1}")

# Streamlit app starts here
st.set_page_config(page_title="Wheel Spinner", layout="centered")
st.title("🎡 Wheel Spinner")

# Select segments
segments = st.slider("🔢 Number of segments", min_value=2, max_value=12, value=6)

# Session state init
if 'running' not in st.session_state:
    st.session_state.running = False
if 'placeholder' not in st.session_state:
    st.session_state.placeholder = st.empty()
if 'wheel' not in st.session_state or st.session_state.wheel.segments != segments:
    st.session_state.wheel = WheelSpinner(segments=segments)

wheel = st.session_state.wheel
placeholder = st.session_state.placeholder

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start"):
        if not st.session_state.running:
            st.session_state.running = True
            wheel.spin_and_animate(placeholder)

with col2:
    if st.button("Stop"):
        if st.session_state.running:
            st.session_state.running = False
            wheel.select_segment(placeholder)

# Initial draw if not running
if not st.session_state.running:
    wheel.draw(placeholder)
