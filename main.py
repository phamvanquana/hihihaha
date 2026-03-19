"""
SAA Learning Hub - Entry Point
An offline course viewer application similar to Coursera/Udemy.
"""
import sys
import os

from PySide6.QtWidgets import (
    QApplication, QFileDialog, QMessageBox, QDialog, 
    QVBoxLayout, QLabel, QPushButton, QWidget
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont

from course_parser import scan_course_folder
from main_window import MainWindow
from styles import DARK_THEME


class WelcomeDialog(QDialog):
    """Welcome dialog for folder selection."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_path = None
        self.setWindowTitle("SAA Learning Hub")
        self.setFixedSize(520, 380)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo / Title
        title = QLabel("☁️  SAA Learning Hub")
        title.setObjectName("welcome_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Your offline course viewer for AWS SAA-C03")
        subtitle.setObjectName("welcome_subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Description
        desc = QLabel(
            "Select the course folder (e.g. 'saa-c03') containing\n"
            "numbered section subfolders with video and text materials."
        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #c0c0d0; font-size: 13px; line-height: 1.5;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        layout.addSpacing(16)
        
        # Browse button
        btn_browse = QPushButton("📂  Open Course Folder")
        btn_browse.setObjectName("btn_open_folder")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.clicked.connect(self._browse_folder)
        layout.addWidget(btn_browse, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel("Supports: MP4 videos, SRT subtitles, HTML & TXT documents")
        footer.setStyleSheet("color: #606080; font-size: 11px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
    
    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Course Folder",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if not folder:
            return
        
        # Validate folder
        sections = scan_course_folder(folder)
        if not sections:
            QMessageBox.warning(
                self,
                "Invalid Folder",
                "The selected folder doesn't contain valid course sections.\n\n"
                "Please select a folder containing numbered subfolders\n"
                "like '1 - Introduction', '2 - Getting Started', etc."
            )
            return
        
        self.selected_path = folder
        self.accept()


def main():
    # High DPI support
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    
    app = QApplication(sys.argv)
    app.setApplicationName("SAALearningHub")
    app.setOrganizationName("Antigravity")
    app.setStyle("Fusion")
    app.setStyleSheet(DARK_THEME)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    settings = QSettings()
    last_path = settings.value("last_course_path", "")
    course_root = ""
    
    # Try to auto-load last folder
    if last_path and os.path.isdir(last_path):
        sections = scan_course_folder(last_path)
        if sections:
            course_root = last_path
        else:
            # Saved path no longer valid for a course
            settings.remove("last_course_path")
    
    if not course_root:
        # Show welcome dialog if no valid path is saved
        welcome = WelcomeDialog()
        result = welcome.exec()
        
        if result != QDialog.Accepted or not welcome.selected_path:
            sys.exit(0)
        
        course_root = welcome.selected_path
        # Save the new successful path
        settings.setValue("last_course_path", course_root)
        sections = scan_course_folder(course_root)
    else:
        # We already have sections from the auto-load check
        pass
    
    # Show main window
    window = MainWindow(sections)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
