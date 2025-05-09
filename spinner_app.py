import streamlit as st
import math
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

# Base Class (Spinner)
class Spinner:
    def _init_(self, segments, radius, center):
        self.angle = 0
        self.selected_index = None
        self.center = center
        self.radius = radius
        self.segments = segments

    def draw(self, placeholder):
        pass

    def spin_once(self, placeholder):
        pass

# Derived Class (WheelSpinner)
class WheelSpinner(Spinner):
    def _init_(self):
        super()._init_(segments=6, radius=140, center=(200, 200))
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

        # Pointer
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

    def spin_once(self, placeholder):
        if st.session_state.running:
            self.angle = (self.angle + self.speed) % 360
            self.draw(placeholder)

    def stop_and_select(self, placeholder):
        st.session_state.running = False
        final_angle = (360 - self.angle) % 360
        segment_angle = 360 / self.segments
        self.selected_index = int(final_angle // segment_angle)
        self.draw(placeholder)
        st.success(f"🎯 Selected Number: {self.selected_index + 1}")

# Page setup
st.set_page_config(page_title="Wheel Spinner", layout="centered")
st.title("🎡 Wheel Spinner")

# Session init
if 'running' not in st.session_state:
    st.session_state.running = False
if 'wheel' not in st.session_state:
    st.session_state.wheel = WheelSpinner()
if 'placeholder' not in st.session_state:
    st.session_state.placeholder = st.empty()

wheel = st.session_state.wheel
placeholder = st.session_state.placeholder

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start"):
        if not st.session_state.running:
            st.session_state.running = True
            wheel.selected_index = None
            wheel.speed = 10

with col2:
    if st.button("Stop"):
        if st.session_state.running:
            wheel.stop_and_select(placeholder)

# Spinning loop
if st.session_state.running:
    wheel.spin_once(placeholder)
    time.sleep(0.05)
    st.experimental_rerun()
else:
    wheel.draw(placeholder)
