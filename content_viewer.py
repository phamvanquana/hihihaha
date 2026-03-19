"""
Content Viewer - Displays HTML and text content for reading lessons.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
from PySide6.QtCore import Qt
from styles import CONTENT_HTML_STYLE


class ContentViewer(QWidget):
    """Displays HTML or plain text content for reading lessons."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Title label
        self.title_label = QLabel("📄 Reading Material")
        self.title_label.setObjectName("transcript_header")
        layout.addWidget(self.title_label)
        
        # Content browser
        self.browser = QTextBrowser()
        self.browser.setObjectName("content_browser")
        self.browser.setOpenExternalLinks(True)
        layout.addWidget(self.browser)
    
    def load_html(self, file_path: str, title: str = ""):
        """Load and display an HTML file."""
        self.title_label.setText(f"📄 {title}" if title else "📄 Reading Material")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception:
                content = "<p>Could not load content.</p>"
        
        # Inject dark theme styles
        styled_content = f"{CONTENT_HTML_STYLE}\n{content}"
        self.browser.setHtml(styled_content)
    
    def load_text(self, file_path: str, title: str = ""):
        """Load and display a plain text file."""
        self.title_label.setText(f"📄 {title}" if title else "📄 Reading Material")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception:
                content = "Could not load content."
        
        # Wrap text in HTML with styling
        escaped = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html = f"{CONTENT_HTML_STYLE}\n<pre style='white-space: pre-wrap;'>{escaped}</pre>"
        self.browser.setHtml(html)
    
    def clear_content(self):
        """Clear the content display."""
        self.browser.clear()
        self.title_label.setText("📄 Reading Material")
