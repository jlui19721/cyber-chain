# @file app/helloworld/pages/factory.py
# @brief

from __future__ import annotations

from typing import assert_never

from app.helloworld.page_id import PageId
from app.helloworld.page_protocol import Page
from app.helloworld.pages.boot import BootPage
from app.helloworld.pages.pet_home import PetHomePage
from app.helloworld.pages.playground import PlaygroundPage
from app.helloworld.pages.music import MusicPage
from app.helloworld.pages.voice import VoicePage
from app.helloworld.pages.notes import NotesPage

class PageFactory:
    """Caches one instance per PageId so e.g. Playground counter persists"""

    def __init__(self) -> None:
        self._cache: dict[PageId, Page] = {}

    def get(self, page_id: PageId) -> Page:
        if page_id not in self._cache:
            self._cache[page_id] = self._create(page_id)
        return self._cache[page_id]

    def _create(self, page_id: PageId) -> Page:
        match page_id:
            case PageId.BOOT:
                return BootPage()
            case PageId.PET_HOME:
                return PetHomePage()
            case PageId.PLAYGROUND:
                return PlaygroundPage()
            case PageId.MUSIC:
                return MusicPage()
            case PageId.VOICE:
                return VoicePage()
            case PageId.NOTES:
                return NotesPage()
            case _:
                assert_never(page_id)