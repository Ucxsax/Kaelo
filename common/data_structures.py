from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class CommandType(Enum):
    CLICK = "click"
    WAIT = "wait"
    END = "end"


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def center(self) -> Point:
        return Point(self.x + self.width // 2, self.y + self.height // 2)


@dataclass
class Element:
    type: str
    rect: Rect
    name: Optional[str] = None
    text: Optional[str] = None


@dataclass
class Command:
    type: CommandType
    target: Optional[Point] = None
    element_name: Optional[str] = None
    wait_time: Optional[float] = None
