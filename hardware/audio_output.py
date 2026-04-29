# @file hardware/audio_output.py
# @brief Protocol for audio output devices (checks for required methods)

from __future__ import annotations

from typing import Protocol

class AudioOutput(Protocol):
    """Plays sound to the active output device (desktop speakers or board DAC)"""

    def play_music_file(self, filename: str) -> None:
        """Play a music file from the filesystem"""

    def pause_music(self) -> None:
        """Pause the current music playback"""

    def shutdown(self)-> None:
        """Release device / mixer resources."""
