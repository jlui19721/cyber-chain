# @file app/helloworld/effects.py
# @brief Effects are actions that can be applied to the current page

from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias

from app.helloworld.page_id import PageId

# @brief Navigate to a different page
# @param page - Page identifier to navigate to
@dataclass(frozen=True)
class Navigate:
    page: PageId

# @brief Log a line of text to the console
# @param text - Text to log
@dataclass(frozen=True)
class LogLine:
    text: str

# @brief Start playing a music file
# @param path - Path to the music file to play
@dataclass(frozen=True)
class StartMusic:
    path: str

# @brief Pause the current music playback
@dataclass(frozen=True)
class PauseMusic:
    pass

Effect: TypeAlias = Navigate | LogLine | StartMusic | PauseMusic
