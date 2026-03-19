"""
Video Player - VLC-based video player widget embedded in Qt.
"""
import sys
import os

# Try to help python-vlc find the DLL on Windows
if sys.platform == "win32":
    vlc_paths = [
        os.environ.get("PYTHON_VLC_LIB_PATH"),
        r"C:\Program Files\VideoLAN\VLC",
        r"C:\Program Files (x86)\VideoLAN\VLC",
    ]
    for path in vlc_paths:
        if path and os.path.isdir(path) and os.path.exists(os.path.join(path, "libvlc.dll")):
            # From Python 3.8+, we need to add the DLL directory explicitly
            if hasattr(os, 'add_dll_directory'):
                try:
                    os.add_dll_directory(path)
                except Exception:
                    pass
            break

import vlc
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QSlider, QLabel, QComboBox, QFrame
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor


class VideoPlayer(QWidget):
    """VLC-based video player widget with playback controls."""
    
    position_changed = Signal(int)  # ms position for transcript sync
    media_ended = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vlc_instance = vlc.Instance('--no-xlib')
        self.player = self.vlc_instance.media_player_new()
        self.is_playing = False
        self.duration = 0
        self._slider_pressed = False
        
        self._setup_ui()
        self._setup_timer()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Video frame
        self.video_frame = QFrame()
        self.video_frame.setObjectName("video_container")
        self.video_frame.setMinimumHeight(360)
        self.video_frame.setStyleSheet("background-color: #000000; border-radius: 8px;")
        layout.addWidget(self.video_frame, 1)
        
        # Controls bar
        controls = QWidget()
        controls.setObjectName("controls_bar")
        controls_layout = QVBoxLayout(controls)
        controls_layout.setContentsMargins(12, 8, 12, 8)
        controls_layout.setSpacing(6)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.sliderPressed.connect(self._on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self._on_slider_released)
        self.progress_slider.sliderMoved.connect(self._on_slider_moved)
        controls_layout.addWidget(self.progress_slider)
        
        # Bottom controls row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10)
        
        # Play button
        self.btn_play = QPushButton("▶")
        self.btn_play.setObjectName("btn_play")
        self.btn_play.setFixedSize(45, 35)
        self.btn_play.clicked.connect(self.toggle_play)
        bottom_row.addWidget(self.btn_play)
        
        # Time label
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("time_label")
        bottom_row.addWidget(self.time_label)
        
        bottom_row.addStretch()
        
        # Speed selector
        speed_label = QLabel("Speed:")
        speed_label.setObjectName("time_label")
        bottom_row.addWidget(speed_label)
        
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "1.75x", "2.0x"])
        self.speed_combo.setCurrentIndex(2)  # 1.0x default
        self.speed_combo.currentTextChanged.connect(self._on_speed_changed)
        bottom_row.addWidget(self.speed_combo)
        
        # Volume
        vol_label = QLabel("🔊")
        vol_label.setObjectName("time_label")
        bottom_row.addWidget(vol_label)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setObjectName("volume_slider")
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        bottom_row.addWidget(self.volume_slider)
        
        controls_layout.addLayout(bottom_row)
        layout.addWidget(controls)
    
    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self._update_ui)
    
    def load_video(self, file_path: str):
        """Load and prepare a video file."""
        media = self.vlc_instance.media_new(file_path)
        self.player.set_media(media)
        
        # Embed video in the Qt frame
        if sys.platform == "win32":
            self.player.set_hwnd(int(self.video_frame.winId()))
        
        self.player.audio_set_volume(self.volume_slider.value())
        self.is_playing = False
        self.btn_play.setText("▶")
        self.progress_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        
        # Auto-play
        self.play()
    
    def play(self):
        """Start playback."""
        self.player.play()
        self.is_playing = True
        self.btn_play.setText("⏸")
        self.timer.start()
        # Apply current speed
        speed_text = self.speed_combo.currentText()
        rate = float(speed_text.replace('x', ''))
        # Delay setting rate slightly so VLC has time to initialize
        QTimer.singleShot(300, lambda: self.player.set_rate(rate))
    
    def pause(self):
        """Pause playback."""
        self.player.pause()
        self.is_playing = False
        self.btn_play.setText("▶")
    
    def toggle_play(self):
        """Toggle between play and pause."""
        if self.is_playing:
            self.pause()
        else:
            self.play()
    
    def seek_to(self, ms: int):
        """Seek to a specific position in milliseconds."""
        self.player.set_time(ms)
    
    def stop(self):
        """Stop playback."""
        self.player.stop()
        self.is_playing = False
        self.btn_play.setText("▶")
        self.timer.stop()
    
    def _update_ui(self):
        """Timer callback to update slider, time label, and emit position."""
        if not self.player.is_playing() and self.is_playing:
            state = self.player.get_state()
            if state == vlc.State.Ended:
                self.is_playing = False
                self.btn_play.setText("▶")
                self.timer.stop()
                self.media_ended.emit()
                return
        
        length = self.player.get_length()
        current = self.player.get_time()
        
        if length > 0:
            self.duration = length
            if not self._slider_pressed:
                pos = int((current / length) * 1000)
                self.progress_slider.setValue(pos)
            
            self.time_label.setText(
                f"{self._format_time(current)} / {self._format_time(length)}"
            )
            self.position_changed.emit(current)
    
    def _on_slider_pressed(self):
        self._slider_pressed = True
    
    def _on_slider_released(self):
        self._slider_pressed = False
        pos = self.progress_slider.value() / 1000.0
        self.player.set_position(pos)
    
    def _on_slider_moved(self, value):
        if self.duration > 0:
            ms = int((value / 1000.0) * self.duration)
            self.time_label.setText(
                f"{self._format_time(ms)} / {self._format_time(self.duration)}"
            )
    
    def _on_speed_changed(self, text):
        rate = float(text.replace('x', ''))
        self.player.set_rate(rate)
    
    def _on_volume_changed(self, value):
        self.player.audio_set_volume(value)
    
    @staticmethod
    def _format_time(ms):
        """Format milliseconds to MM:SS or HH:MM:SS."""
        if ms < 0:
            ms = 0
        seconds = ms // 1000
        minutes = seconds // 60
        hours = minutes // 60
        seconds %= 60
        minutes %= 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
