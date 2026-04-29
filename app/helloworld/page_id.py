# @file app/helloworld/page_id.py
# @brief Enumeration of all possible pages in the HelloWorld application

from __future__ import annotations

from enum import Enum, auto

class PageId(Enum):
    BOOT = auto()
    PET_HOME = auto()
    PLAYGROUND = auto()
    MUSIC = auto()
    VOICE = auto()
    NOTES = auto()
