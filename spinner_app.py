import streamlit as st
import math
import time
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from abc import ABC, abstractmethod

# Abstract Base Class
class Spinner(ABC):
    def __init__(self, segments, radius, center):
        self.angle = 0
        self.selected_index = None
        self.center = center
        self.radius = radius
        self.segments = segments

    @abstractmethod
    def draw(self, placeholder):
        pass

    @abstractmethod
    def start(self, placeholder):
        pass

    @abstractmethod
    def stop(self, placeholder):
        pass

# Wheel Spinner
class WheelSpinner(Spinner):
    def __init__(self):
        super().__init__(segments=6, radius=140, center=(200, 200))
        self.base_colors = ["#b3e5fc", "#81d4fa", "#4fc3f7", "#29b6f6", "#03a9f4", "#039be5"]

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

    def start(self, placeholder):
        if not st.session_state.running:
            st.session_state.running = True
            self.selected_index = None
            st.session_state.speed = 15

        while st.session_state.running:
            self.angle = (self.angle + st.session_state.speed) % 360
            self.draw(placeholder)
            time.sleep(0.05)
            st.session_state.speed = max(1, st.session_state.speed - 0.1)

    def stop(self, placeholder):
        st.session_state.running = False

        # Randomly stop at any angle
        final_angle = random.uniform(0, 360)
        self.angle = (360 - final_angle) % 360

        segment_angle = 360 / self.segments
        self.selected_index = int(final_angle // segment_angle)
        selected_number = self.selected_index + 1

        self.draw(placeholder)
        st.success(f"🎯 Selected Number: {selected_number}")

# Streamlit setup
st.set_page_config(page_title="Wheel Spinner", layout="centered")
st.title("🎡 Randomized Wheel Spinner (OOP + Abstract Class)")

# Session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'speed' not in st.session_state:
    st.session_state.speed = 15

# Custom CSS
st.markdown("""
    <style>
    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
    }
    .spinner {
        border: 16px solid #f3f3f3;
        border-top: 16px solid #3498db;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
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

# Spinner logic
wheel = WheelSpinner()
placeholder = st.empty()

col1, col2 = st.columns(2)
with col1:
    if st.button("Start") and not st.session_state.running:
        wheel.start(placeholder)

with col2:
    if st.button("Stop") and st.session_state.running:
        wheel.stop(placeholder)

if st.session_state.running:
    st.markdown("""
    <div class="spinner-container">
        <div class="spinner"></div>
    </div>
    <p style="text-align:center; font-size:20px;">Spinning...🎯</p>
    """, unsafe_allow_html=True)

if not st.session_state.running:
    wheel.draw(placeholder)
