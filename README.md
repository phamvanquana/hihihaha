# ☁️ Learning Hub

Learning Hub is a premium offline course viewer designed specifically for the course materials. It provides a professional, distraction-free environment for learning, similar to C or U, but entirely offline.

## ✨ Features

- **📂 Offline Course Parsing**: Automatically organizes and displays course content from standard numbered folders.
- **🎥 Premium Video Player**: Integration with VLC for high-quality playback with play/pause, seek, volume, and playback speed controls.
- **📜 Sync Transcript**: Real-time subtitle synchronization with the video, allowing you to click a line to jump to that timestamp.
- **🌗 Dark Theme**: Elegant, high-contrast dark mode with AWS-inspired orange accents for comfortable long-term viewing.
- **🛠️ Persistence & Progress**: Automatically remembers your last used course folder and exactly where you left off in your learning journey.
- **📊 Progress Bar**: Real-time status bar showing your current lesson and overall course completion percentage.
- **⛶ Theater Mode**: A distraction-free fullscreen mode that hides all UI elements except for the video content.
- **📄 Multi-format Support**: View HTML cheat sheets and plaintext notes directly within the app.

## 🛠️ System Requirements

- **Operating System**: Windows (tested on Windows 10/11).
- **Python**: Version 3.11 or higher.
- **VLC Player**: **CRITICAL** - You MUST have the **64-bit version of VLC Media Player** installed on your system. The 32-bit version is incompatible with the 64-bit Python environment.
  - [Download 64-bit VLC](https://www.videolan.org/vlc/) (Select "Windows 64-bit").

## 📦 Dependencies

The application relies on the following Python libraries:

1.  **PySide6**: Qt6 framework for the high-performance UI.
2.  **python-vlc**: Python bindings for the VLC media player.
3.  **pysrt**: For parsing and synchronizing SubRip subtitle files.

Install them all via pip:
```bash
pip install PySide6 python-vlc pysrt
```

## 🚀 How to Run

### Option 1: Run from Source
If you have Python and the dependencies installed:
```bash
python main.py
```

### Option 2: Run Portable Executable
If you have built the application using the instructions below, you can simply run:
`compiled/SAA_Learning_Hub.exe`

## 🏗️ How to Build (.exe)

### Option 1: Using the provided Batch File (Recommended)
Simply double-click `build.bat` in the root directory. This will automatically run PyInstaller with the correct `.spec` configuration and output the result to the `compiled/` folder.

### Option 2: Manual Command
Alternatively, you can run the following command in your terminal:
```bash
python -m PyInstaller --noconfirm --distpath "./compiled" --workpath "./build_temp" SAA_Learning_Hub.spec
```
The output executable will be generated in the `compiled/` directory.

## 📖 Usage Guide

1.  **Select Folder**: On first launch, select the folder containing your SAA-C03 course materials. The app expects numbered subfolders (e.g., `1 - Introduction`, `2 - Getting Started`).
2.  **Navigation**: Use the left sidebar to navigate sections and lessons. Use the `Prev` and `Next` buttons at the top to move between lessons.
3.  **Fullscreen**: Click the `⛶` button or press **Esc** to toggle the theater mode. You can also press **Esc** to exit fullscreen at any time.
4.  **Settings**: Click the **⚙️ Settings** icon in the sidebar to change your course root folder or see your current path.

## ⚖️ License
Personal learning tool. All brand names and course contents are the property of their respective owners.
