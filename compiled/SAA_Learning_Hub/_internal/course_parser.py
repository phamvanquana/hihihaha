"""
Course Parser - Scans folder structure and builds course data model.
"""
import os
import re
from dataclasses import dataclass, field


@dataclass
class Lesson:
    number: int
    title: str
    lesson_type: str  # "video" or "reading"
    video_path: str = ""
    srt_path: str = ""
    content_path: str = ""
    section_number: int = 0

    @property
    def display_title(self):
        return f"{self.section_number}.{self.number} - {self.title}"


@dataclass
class Section:
    number: int
    title: str
    folder_path: str
    lessons: list = field(default_factory=list)

    @property
    def display_title(self):
        return f"Section {self.number}: {self.title}"


def parse_section_folder_name(folder_name: str):
    """Parse folder name like '10 - Route 53' into (number, title)."""
    match = re.match(r'^(\d+)\s*-\s*(.+)$', folder_name)
    if match:
        return int(match.group(1)), match.group(2).strip()
    return None, None


def parse_lesson_file_name(file_name: str):
    """Parse file name like '103 - What is a DNS.en.srt' into (number, title, extension)."""
    # Remove extension(s)
    base = file_name
    ext = ""
    
    # Handle compound extensions like .en.srt
    if file_name.endswith('.en.srt'):
        base = file_name[:-7]
        ext = '.en.srt'
    else:
        base, ext = os.path.splitext(file_name)
    
    match = re.match(r'^(\d+)\s*-\s*(.+)$', base)
    if match:
        return int(match.group(1)), match.group(2).strip(), ext
    return None, None, ext


def scan_course_folder(root_path: str) -> list:
    """
    Scan the root course folder and return a list of Section objects.
    Each section contains its lessons sorted by lesson number.
    """
    sections = []
    
    if not os.path.isdir(root_path):
        return sections
    
    # Get all subdirectories
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if not os.path.isdir(item_path):
            continue
        
        section_num, section_title = parse_section_folder_name(item)
        if section_num is None:
            continue
        
        section = Section(
            number=section_num,
            title=section_title,
            folder_path=item_path
        )
        
        # Scan files in this section folder
        files_by_lesson = {}
        for file_name in os.listdir(item_path):
            file_path = os.path.join(item_path, file_name)
            if not os.path.isfile(file_path):
                continue
            
            lesson_num, lesson_title, ext = parse_lesson_file_name(file_name)
            if lesson_num is None:
                continue
            
            if lesson_num not in files_by_lesson:
                files_by_lesson[lesson_num] = {
                    'title': lesson_title,
                    'video': None,
                    'srt': None,
                    'html': None,
                    'txt': None,
                }
            
            entry = files_by_lesson[lesson_num]
            ext_lower = ext.lower()
            
            if ext_lower == '.mp4':
                entry['video'] = file_path
                entry['title'] = lesson_title  # Prefer video title
            elif ext_lower == '.en.srt' or ext_lower == '.srt':
                entry['srt'] = file_path
            elif ext_lower == '.html':
                entry['html'] = file_path
                if not entry['title']:
                    entry['title'] = lesson_title
            elif ext_lower == '.txt':
                entry['txt'] = file_path
                if not entry['title']:
                    entry['title'] = lesson_title
        
        # Build lessons from grouped files
        # Determine local lesson index within section
        sorted_lesson_nums = sorted(files_by_lesson.keys())
        for local_idx, lesson_num in enumerate(sorted_lesson_nums, start=1):
            data = files_by_lesson[lesson_num]
            
            if data['video']:
                lesson = Lesson(
                    number=local_idx,
                    title=data['title'],
                    lesson_type='video',
                    video_path=data['video'],
                    srt_path=data['srt'] or '',
                    section_number=section_num,
                )
                section.lessons.append(lesson)
            
            # If there's an HTML or TXT file WITHOUT a matching video, it's a reading lesson
            if data['html'] and not data['video']:
                lesson = Lesson(
                    number=local_idx,
                    title=data['title'],
                    lesson_type='reading',
                    content_path=data['html'],
                    section_number=section_num,
                )
                section.lessons.append(lesson)
            elif data['txt'] and not data['video']:
                lesson = Lesson(
                    number=local_idx,
                    title=data['title'],
                    lesson_type='reading',
                    content_path=data['txt'],
                    section_number=section_num,
                )
                section.lessons.append(lesson)
        
        if section.lessons:
            sections.append(section)
    
    # Sort sections by number
    sections.sort(key=lambda s: s.number)
    return sections


def get_all_lessons_flat(sections: list) -> list:
    """Return a flat list of all lessons across all sections, in order."""
    lessons = []
    for section in sections:
        lessons.extend(section.lessons)
    return lessons
