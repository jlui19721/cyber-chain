# @file services/buttonevent.py
# @brief ButtonEvent & ButtonEdge classes
# `ButtonEvent` lists possible actions on a button (press, release, & hold)
# `ButtonEdge` lists possible states of a button (down, up)

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
    HOLD = auto()     # button is held down for 2 sec

@dataclass(frozen=True)
class ButtonEvent:
    button: ButtonId
    kind: ButtonEventKind

class ButtonEdge(Enum):
    DOWN = auto()
    UP   = auto()

@dataclass(frozen=True)
class RawButtonEdge:
    button: ButtonId
    edge: ButtonEdge
