from dataclasses import dataclass
from enum import Enum, auto

class ButtonId(Enum):
    A = auto()
    B = auto()
    X = auto()
    Y = auto()

class ButtonEventKind(Enum):
    PRESS = auto()    # 0 → 1
    RELEASE = auto()  # 1 → 0

@dataclass(frozen=True)
class ButtonEvent:
    button: ButtonId
    kind: ButtonEventKind
