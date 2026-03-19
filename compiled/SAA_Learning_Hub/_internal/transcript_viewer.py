"""
Transcript Viewer - Displays SRT subtitles with sync highlighting.
"""
import pysrt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QFont


class TranscriptViewer(QWidget):
    """Displays SRT transcript with highlighted current subtitle."""
    
    seek_requested = Signal(int)  # ms position to seek to
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.subs = []
        self.sub_positions = []  # (start_ms, end_ms, text, block_start)
        self.current_highlight_idx = -1
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Header
        header = QLabel("📝 Transcript")
        header.setObjectName("transcript_header")
        layout.addWidget(header)
        
        # Transcript text area
        self.text_area = QTextEdit()
        self.text_area.setObjectName("transcript_area")
        self.text_area.setReadOnly(True)
        self.text_area.setMinimumHeight(120)
        self.text_area.mousePressEvent = self._on_click
        layout.addWidget(self.text_area)
    
    def load_srt(self, srt_path: str):
        """Load and display an SRT file."""
        self.subs = []
        self.sub_positions = []
        self.current_highlight_idx = -1
        self.text_area.clear()
        
        if not srt_path:
            self.text_area.setPlainText("No transcript available for this lesson.")
            return
        
        try:
            subs = pysrt.open(srt_path, encoding='utf-8')
        except Exception:
            try:
                subs = pysrt.open(srt_path, encoding='latin-1')
            except Exception:
                self.text_area.setPlainText("Could not load transcript.")
                return
        
        self.subs = subs
        
        # Build transcript text with timestamps
        lines = []
        char_pos = 0
        for sub in subs:
            start_ms = (sub.start.hours * 3600 + sub.start.minutes * 60 + 
                       sub.start.seconds) * 1000 + sub.start.milliseconds
            end_ms = (sub.end.hours * 3600 + sub.end.minutes * 60 + 
                     sub.end.seconds) * 1000 + sub.end.milliseconds
            
            # Format timestamp
            time_str = f"[{sub.start.hours:02d}:{sub.start.minutes:02d}:{sub.start.seconds:02d}]"
            text = sub.text.replace('\n', ' ')
            line = f"{time_str}  {text}"
            
            self.sub_positions.append({
                'start_ms': start_ms,
                'end_ms': end_ms,
                'text': text,
                'line_start': char_pos,
                'line_length': len(line),
            })
            
            lines.append(line)
            char_pos += len(line) + 1  # +1 for newline
        
        self.text_area.setPlainText('\n'.join(lines))
    
    def update_position(self, ms: int):
        """Highlight the current subtitle based on playback position."""
        if not self.sub_positions:
            return
        
        # Find current subtitle
        new_idx = -1
        for i, sp in enumerate(self.sub_positions):
            if sp['start_ms'] <= ms <= sp['end_ms']:
                new_idx = i
                break
        
        if new_idx == self.current_highlight_idx:
            return
        
        self.current_highlight_idx = new_idx
        
        # Reset all formatting
        cursor = self.text_area.textCursor()
        cursor.select(QTextCursor.Document)
        normal_fmt = QTextCharFormat()
        normal_fmt.setBackground(QColor("transparent"))
        normal_fmt.setForeground(QColor("#c0c0d0"))
        cursor.setCharFormat(normal_fmt)
        
        # Highlight current
        if new_idx >= 0:
            sp = self.sub_positions[new_idx]
            cursor.setPosition(sp['line_start'])
            cursor.setPosition(sp['line_start'] + sp['line_length'], QTextCursor.KeepAnchor)
            
            highlight_fmt = QTextCharFormat()
            highlight_fmt.setBackground(QColor(255, 153, 0, 40))
            highlight_fmt.setForeground(QColor("#FF9900"))
            font = QFont()
            font.setBold(True)
            highlight_fmt.setFont(font)
            cursor.setCharFormat(highlight_fmt)
            
            # Auto-scroll to current subtitle
            cursor.setPosition(sp['line_start'])
            self.text_area.setTextCursor(cursor)
            self.text_area.ensureCursorVisible()
    
    def _on_click(self, event):
        """Handle click on transcript to seek video."""
        # Get cursor position from click
        cursor = self.text_area.cursorForPosition(event.pos())
        pos = cursor.position()
        
        # Find which subtitle was clicked
        for sp in self.sub_positions:
            if sp['line_start'] <= pos <= sp['line_start'] + sp['line_length']:
                self.seek_requested.emit(sp['start_ms'])
                break
        
        # Call original mousePressEvent
        QTextEdit.mousePressEvent(self.text_area, event)
    
    def clear_transcript(self):
        """Clear the transcript display."""
        self.subs = []
        self.sub_positions = []
        self.current_highlight_idx = -1
        self.text_area.clear()
