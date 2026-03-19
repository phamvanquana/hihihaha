"""
Main Window - Primary application window with sidebar and content area.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QTreeWidget, QTreeWidgetItem, QStackedWidget,
    QPushButton, QLabel, QFrame, QScrollArea, QStatusBar,
    QFileDialog, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtGui import QIcon, QFont, QShortcut, QKeySequence

from course_parser import Section, Lesson, get_all_lessons_flat, scan_course_folder
from video_player import VideoPlayer
from transcript_viewer import TranscriptViewer
from content_viewer import ContentViewer


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, sections: list, parent=None):
        super().__init__(parent)
        self.sections = sections
        self.all_lessons = get_all_lessons_flat(sections)
        self.current_lesson_index = -1
        self.lesson_tree_items = {}  # Maps (section_idx, lesson_idx) -> QTreeWidgetItem
        
        self.setWindowTitle("SAA Learning Hub")
        self.setMinimumSize(1200, 750)
        self.resize(1400, 850)
        
        self._setup_ui()
        self._setup_status_bar()
        
        # Load progress
        settings = QSettings()
        start_index = settings.value("last_lesson_index", 0, type=int)
        
        # Load the saved lesson or the first one
        if self.all_lessons:
            if 0 <= start_index < len(self.all_lessons):
                self._load_lesson(start_index)
            else:
                self._load_lesson(0)
            
        # Global shortcuts
        self.fs_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.fs_shortcut.activated.connect(self._on_esc_pressed)
    
    def _on_esc_pressed(self):
        if self.isFullScreen():
            self._toggle_fullscreen()
    
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # ============ LEFT SIDEBAR ============
        self.sidebar_container = QWidget()
        self.sidebar_container.setObjectName("sidebar")
        self.sidebar_container.setFixedWidth(340)
        sidebar_layout = QVBoxLayout(self.sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # App title
        title_label = QLabel("☁️  SAA Learning Hub")
        title_label.setObjectName("app_title")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_label.setFixedHeight(56)
        sidebar_layout.addWidget(title_label)
        
        # Course progress label
        total = len(self.all_lessons)
        self.progress_label = QLabel(f"  📚 {total} lessons across {len(self.sections)} sections")
        self.progress_label.setStyleSheet("color: #a0a0c0; padding: 8px 12px; font-size: 11px;")
        sidebar_layout.addWidget(self.progress_label)
        
        # Course tree
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(20)
        self.tree.setAnimated(True)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.itemClicked.connect(self._on_tree_item_clicked)
        sidebar_layout.addWidget(self.tree)
        
        self._populate_tree()
        
        # Bottom sidebar buttons (Settings)
        sidebar_bottom = QHBoxLayout()
        sidebar_bottom.setContentsMargins(10, 10, 10, 10)
        
        self.btn_settings = QPushButton("⚙️ Settings")
        self.btn_settings.setObjectName("btn_settings")
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.clicked.connect(self._show_settings)
        sidebar_bottom.addWidget(self.btn_settings)
        
        sidebar_layout.addLayout(sidebar_bottom)
        
        splitter.addWidget(self.sidebar_container)
        
        # ============ RIGHT CONTENT AREA ============
        content_widget = QWidget()
        content_widget.setObjectName("content_area")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 12, 16, 12)
        content_layout.setSpacing(8)
        
        # Lesson header
        self.header_widget = QWidget()
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)
        
        self.section_label = QLabel("")
        self.section_label.setObjectName("section_label")
        header_layout.addWidget(self.section_label)
        
        self.lesson_title_label = QLabel("Select a lesson to begin")
        self.lesson_title_label.setObjectName("lesson_title_label")
        self.lesson_title_label.setWordWrap(True)
        header_layout.addWidget(self.lesson_title_label)
        
        content_layout.addWidget(self.header_widget)
        
        # Stacked widget for video player / content viewer
        self.content_stack = QStackedWidget()
        
        # Page 0: Video player + transcript
        video_page = QWidget()
        video_page_layout = QVBoxLayout(video_page)
        video_page_layout.setContentsMargins(0, 0, 0, 0)
        
        # Use a vertical splitter for video vs transcript
        self.video_splitter = QSplitter(Qt.Vertical)
        
        self.video_player = VideoPlayer()
        self.video_player.position_changed.connect(self._on_video_position_changed)
        self.video_player.media_ended.connect(self._on_media_ended)
        self.video_player.fullscreen_requested.connect(self._toggle_fullscreen)
        self.video_splitter.addWidget(self.video_player)
        
        self.transcript_viewer = TranscriptViewer()
        self.transcript_viewer.seek_requested.connect(self._on_transcript_seek)
        self.video_splitter.addWidget(self.transcript_viewer)
        
        # Set initial sizes (70% video, 30% transcript)
        self.video_splitter.setStretchFactor(0, 3)
        self.video_splitter.setStretchFactor(1, 1)
        
        video_page_layout.addWidget(self.video_splitter)
        
        self.content_stack.addWidget(video_page)
        
        # Page 1: Content viewer (HTML/text)
        content_page = QWidget()
        content_page_layout = QVBoxLayout(content_page)
        content_page_layout.setContentsMargins(0, 0, 0, 0)
        
        self.content_viewer = ContentViewer()
        content_page_layout.addWidget(self.content_viewer)
        
        self.content_stack.addWidget(content_page)
        
        content_layout.addWidget(self.content_stack, 1)
        
        # Navigation bar
        self.nav_bar = QWidget()
        self.nav_bar.setObjectName("nav_bar")
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(8, 6, 8, 6)
        
        self.btn_prev = QPushButton("◀  Previous")
        self.btn_prev.setObjectName("btn_prev")
        self.btn_prev.clicked.connect(self._go_previous)
        nav_layout.addWidget(self.btn_prev)
        
        nav_layout.addStretch()
        
        self.nav_info_label = QLabel("")
        self.nav_info_label.setStyleSheet("color: #a0a0c0; font-size: 12px;")
        self.nav_info_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(self.nav_info_label)
        
        nav_layout.addStretch()
        
        self.btn_next = QPushButton("Next  ▶")
        self.btn_next.setObjectName("btn_next")
        self.btn_next.clicked.connect(self._go_next)
        nav_layout.addWidget(self.btn_next)
        
        content_layout.addWidget(self.nav_bar)
        
        splitter.addWidget(content_widget)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
    
    def _populate_tree(self):
        """Populate the sidebar tree with sections and lessons."""
        self.tree.clear()
        self.lesson_tree_items = {}
        
        for s_idx, section in enumerate(self.sections):
            # Section item
            section_item = QTreeWidgetItem(self.tree)
            section_item.setText(0, f"📁 {section.display_title}")
            section_item.setData(0, Qt.UserRole, ('section', s_idx))
            
            # Set section font
            font = section_item.font(0)
            font.setBold(True)
            font.setPointSize(10)
            section_item.setFont(0, font)
            
            # Lesson items
            for l_idx, lesson in enumerate(section.lessons):
                lesson_item = QTreeWidgetItem(section_item)
                icon = "🎬" if lesson.lesson_type == 'video' else "📄"
                lesson_item.setText(0, f"  {icon} {lesson.display_title}")
                lesson_item.setData(0, Qt.UserRole, ('lesson', s_idx, l_idx))
                
                # Store reference for highlighting
                self.lesson_tree_items[(s_idx, l_idx)] = lesson_item
        
        # Expand the first section
        if self.tree.topLevelItemCount() > 0:
            self.tree.topLevelItem(0).setExpanded(True)
    
    def _on_tree_item_clicked(self, item, column):
        """Handle sidebar tree item click."""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        if data[0] == 'section':
            # Toggle expansion
            item.setExpanded(not item.isExpanded())
        elif data[0] == 'lesson':
            s_idx, l_idx = data[1], data[2]
            # Find flat index
            flat_idx = 0
            for i in range(s_idx):
                flat_idx += len(self.sections[i].lessons)
            flat_idx += l_idx
            self._load_lesson(flat_idx)
    
    def _load_lesson(self, flat_index: int):
        """Load a lesson by its flat index."""
        if flat_index < 0 or flat_index >= len(self.all_lessons):
            return
        
        # Stop any playing video
        if self.current_lesson_index >= 0:
            self.video_player.stop()
        
        self.current_lesson_index = flat_index
        lesson = self.all_lessons[flat_index]
        
        # Find section for this lesson
        section = None
        for s in self.sections:
            if lesson in s.lessons:
                section = s
                break
        
        # Update header
        if section:
            self.section_label.setText(f"📁 {section.display_title}")
        self.lesson_title_label.setText(lesson.title)
        
        self.nav_info_label.setText(f"Lesson {flat_index + 1} of {len(self.all_lessons)}")
        self.btn_prev.setEnabled(flat_index > 0)
        self.btn_next.setEnabled(flat_index < len(self.all_lessons) - 1)
        
        # Save progress
        QSettings().setValue("last_lesson_index", flat_index)
        
        # Update status bar
        self._update_status_bar()
        
        # Load content
        if lesson.lesson_type == 'video':
            self.content_stack.setCurrentIndex(0)
            self.video_player.load_video(lesson.video_path)
            self.transcript_viewer.load_srt(lesson.srt_path)
        else:
            self.content_stack.setCurrentIndex(1)
            if lesson.content_path.lower().endswith('.html'):
                self.content_viewer.load_html(lesson.content_path, lesson.title)
            else:
                self.content_viewer.load_text(lesson.content_path, lesson.title)
        
        # Highlight in tree
        self._highlight_current_lesson(lesson)
    
    def _highlight_current_lesson(self, lesson: Lesson):
        """Highlight the current lesson in the sidebar tree."""
        # Find (s_idx, l_idx) for this lesson
        for (s_idx, l_idx), item in self.lesson_tree_items.items():
            section = self.sections[s_idx]
            if l_idx < len(section.lessons) and section.lessons[l_idx] is lesson:
                # Select this item
                self.tree.setCurrentItem(item)
                # Ensure section is expanded
                parent = item.parent()
                if parent:
                    parent.setExpanded(True)
                # Scroll to it
                self.tree.scrollToItem(item)
                break
    
    def _on_video_position_changed(self, ms: int):
        """Sync transcript with video position."""
        self.transcript_viewer.update_position(ms)
    
    def _on_transcript_seek(self, ms: int):
        """Seek video when transcript line is clicked."""
        self.video_player.seek_to(ms)
    
    def _on_media_ended(self):
        """Auto-advance to next lesson when video ends."""
        # Don't auto-advance, just stop
        pass
    
    def _go_previous(self):
        """Navigate to previous lesson."""
        if self.current_lesson_index > 0:
            self._load_lesson(self.current_lesson_index - 1)
    
    def _go_next(self):
        """Navigate to next lesson."""
        if self.current_lesson_index < len(self.all_lessons) - 1:
            self._load_lesson(self.current_lesson_index + 1)
    
    def _toggle_fullscreen(self):
        """Hide/Show UI elements for a better fullscreen experience."""
        is_fs = not self.isFullScreen()
        
        if is_fs:
            # Enter Fullscreen
            self.showFullScreen()
            self.sidebar_container.hide()
            self.transcript_viewer.hide()
            self.nav_bar.hide()
            self.header_widget.hide()
        else:
            # Exit Fullscreen
            self.showNormal()
            self.sidebar_container.show()
            self.transcript_viewer.show()
            self.nav_bar.show()
            self.header_widget.show()
        
        # Update video player icon
        self.video_player.update_fullscreen_icon(is_fs)
    
    def _on_esc_pressed(self):
        """Exit fullscreen on Esc key."""
        if self.isFullScreen():
            self._toggle_fullscreen()
            
    def _setup_status_bar(self):
        """Initialize the status bar."""
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("status_bar")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _update_status_bar(self):
        """Update progress info in the status bar."""
        if self.current_lesson_index < 0:
            return
            
        lesson = self.all_lessons[self.current_lesson_index]
        progress = ((self.current_lesson_index + 1) / len(self.all_lessons)) * 100
        
        msg = f"Current: {lesson.title}    |    Progress: {self.current_lesson_index + 1} / {len(self.all_lessons)} ({progress:.1f}%)"
        self.status_bar.showMessage(msg)

    def _show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        if dialog.exec():
            # If settings changed, we might need to reload
            if dialog.new_path:
                try:
                    sections = scan_course_folder(dialog.new_path)
                    if sections:
                        self.sections = sections
                        self.all_lessons = get_all_lessons_flat(sections)
                        self._populate_tree()
                        self._load_lesson(0)
                        QMessageBox.information(self, "Success", "Course folder updated successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load new course: {e}")

    def closeEvent(self, event):
        """Clean up VLC on close."""
        self.video_player.stop()
        super().closeEvent(event)


class SettingsDialog(QDialog):
    """Dialog to manage application settings."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_win = parent
        self.new_path = None
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 300)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)
        
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FF9900;")
        layout.addWidget(title)
        
        # Course Path Section
        path_label = QLabel("Course Root Directory:")
        layout.addWidget(path_label)
        
        settings = QSettings()
        current_path = settings.value("last_course_path", "")
        
        self.path_edit = QLabel(current_path)
        self.path_edit.setWordWrap(True)
        self.path_edit.setStyleSheet("background: #1a1a2e; padding: 8px; border-radius: 4px; border: 1px solid #303050;")
        layout.addWidget(self.path_edit)
        
        btn_change = QPushButton("Change Folder...")
        btn_change.setCursor(Qt.PointingHandCursor)
        btn_change.clicked.connect(self._change_folder)
        layout.addWidget(btn_change, alignment=Qt.AlignLeft)
        
        layout.addStretch()
        
        # Close button
        btn_done = QPushButton("Done")
        btn_done.setFixedWidth(100)
        btn_done.clicked.connect(self.accept)
        layout.addWidget(btn_done, alignment=Qt.AlignRight)
        
    def _change_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Course Folder",
            self.path_edit.text(),
            QFileDialog.ShowDirsOnly
        )
        
        if folder:
            self.new_path = folder
            self.path_edit.setText(folder)
            QSettings().setValue("last_course_path", folder)
