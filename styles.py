"""
Styles - Dark theme stylesheet for the application.
"""

DARK_THEME = """
/* =============== GLOBAL =============== */
QMainWindow, QDialog {
    background-color: #0f0e17;
    color: #e0e0e0;
}

QWidget {
    color: #e0e0e0;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}

/* =============== SIDEBAR =============== */
#sidebar {
    background-color: #1a1a2e;
    border-right: 1px solid #2a2a4a;
}

#app_title {
    color: #FF9900;
    font-size: 20px;
    font-weight: bold;
    padding: 16px 12px;
    background-color: #12122a;
    border-bottom: 2px solid #FF9900;
}

QTreeWidget {
    background-color: #1a1a2e;
    border: none;
    outline: none;
    padding: 4px;
}

QTreeWidget::item {
    padding: 8px 8px;
    border-radius: 6px;
    margin: 1px 4px;
    color: #c0c0d0;
}

QTreeWidget::item:hover {
    background-color: #252545;
    color: #ffffff;
}

QTreeWidget::item:selected {
    background-color: rgba(255, 153, 0, 0.15);
    color: #FF9900;
    border-left: 3px solid #FF9900;
}

QTreeWidget::branch {
    background-color: #1a1a2e;
}

QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {
    image: none;
}

QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings {
    image: none;
}

QHeaderView::section {
    background-color: #1a1a2e;
    border: none;
}

/* =============== CONTENT AREA =============== */
#content_area {
    background-color: #16213e;
}

#video_container {
    background-color: #000000;
    border-radius: 8px;
}

/* =============== CONTROLS BAR =============== */
#controls_bar {
    background-color: #1a1a3e;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0px;
}

QPushButton {
    background-color: #2a2a5a;
    color: #e0e0e0;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #3a3a6a;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #FF9900;
    color: #0f0e17;
}

#btn_play {
    background-color: #FF9900;
    color: #0f0e17;
    font-size: 16px;
    font-weight: bold;
    min-width: 45px;
    min-height: 35px;
    border-radius: 8px;
}

#btn_play:hover {
    background-color: #FFB347;
}

#btn_prev, #btn_next {
    background-color: rgba(255, 153, 0, 0.2);
    color: #FF9900;
    font-weight: bold;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 14px;
}

#btn_prev:hover, #btn_next:hover {
    background-color: rgba(255, 153, 0, 0.35);
    color: #FFB347;
}

/* =============== SLIDER =============== */
QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background: #2a2a5a;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #FF9900;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #FFB347;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::sub-page:horizontal {
    background: #FF9900;
    border-radius: 3px;
}

/* =============== COMBO BOX =============== */
QComboBox {
    background-color: #2a2a5a;
    color: #e0e0e0;
    border: 1px solid #3a3a6a;
    border-radius: 6px;
    padding: 4px 8px;
    min-width: 65px;
}

QComboBox:hover {
    border-color: #FF9900;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #2a2a5a;
    color: #e0e0e0;
    selection-background-color: #FF9900;
    selection-color: #0f0e17;
    border: 1px solid #3a3a6a;
    border-radius: 4px;
}

/* =============== LABEL =============== */
#time_label {
    color: #a0a0c0;
    font-size: 12px;
    font-family: "Consolas", monospace;
}

#lesson_title_label {
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    padding: 8px 0px;
}

#section_label {
    color: #a0a0c0;
    font-size: 12px;
    padding: 2px 0px;
}

/* =============== TRANSCRIPT =============== */
#transcript_header {
    color: #FF9900;
    font-size: 15px;
    font-weight: bold;
    padding: 8px 0px 4px 0px;
    border-top: 1px solid #2a2a4a;
}

#transcript_area {
    background-color: #12122a;
    color: #c0c0d0;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
    line-height: 1.6;
}

/* =============== CONTENT VIEWER =============== */
#content_browser {
    background-color: #12122a;
    color: #e0e0e0;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 16px;
    font-size: 14px;
}

/* =============== SCROLL BARS =============== */
QScrollBar:vertical {
    background: #1a1a2e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #3a3a6a;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #FF9900;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #1a1a2e;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: #3a3a6a;
    min-width: 30px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background: #FF9900;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* =============== VOLUME =============== */
#volume_slider {
    max-width: 100px;
}

/* =============== WELCOME SCREEN =============== */
#welcome_widget {
    background-color: #16213e;
}

#welcome_title {
    color: #FF9900;
    font-size: 28px;
    font-weight: bold;
}

#welcome_subtitle {
    color: #a0a0c0;
    font-size: 14px;
}

#btn_open_folder {
    background-color: #FF9900;
    color: #0f0e17;
    font-size: 16px;
    font-weight: bold;
    padding: 14px 36px;
    border-radius: 10px;
    min-width: 200px;
}

#btn_open_folder:hover {
    background-color: #FFB347;
}

/* =============== SPLITTER =============== */
QSplitter::handle {
    background-color: #2a2a4a;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #FF9900;
}

/* =============== NAV BAR =============== */
#nav_bar {
    background-color: #1a1a3e;
    border-radius: 8px;
    padding: 6px 8px;
}

#btn_settings {
    background-color: transparent;
    border: 1px solid #404060;
    color: #c0c0d0;
    border-radius: 4px;
    font-size: 13px;
    padding: 6px 12px;
}
#btn_settings:hover {
    background-color: #303050;
    border-color: #FF9900;
    color: white;
}

QStatusBar {
    background-color: #0f0e17;
    color: #8080a0;
    border-top: 1px solid #2a2a4a;
    font-size: 11px;
}
QStatusBar::item {
    border: none;
}
"""

CONTENT_HTML_STYLE = """
<style>
    body {
        background-color: #12122a;
        color: #e0e0e0;
        font-family: "Segoe UI", "Inter", sans-serif;
        font-size: 14px;
        line-height: 1.7;
        padding: 16px;
    }
    h1, h2, h3 { color: #FF9900; }
    a { color: #64b5f6; }
    code {
        background-color: #2a2a5a;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: "Consolas", monospace;
    }
    pre {
        background-color: #2a2a5a;
        padding: 12px;
        border-radius: 8px;
        overflow-x: auto;
    }
    ul, ol { padding-left: 24px; }
    li { margin-bottom: 4px; }
    img { max-width: 100%; border-radius: 8px; }
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid #3a3a6a;
        padding: 8px 12px;
        text-align: left;
    }
    th { background-color: #2a2a5a; color: #FF9900; }
</style>
"""
