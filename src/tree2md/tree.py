from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from typing import Any
from dataclasses import dataclass

@dataclass
class Content:
    type: str
    name: str
    contents: List[Content] = field(default_factory=list)

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> 'Content':
        return cls(
            type=obj["type"],
            name=obj["name"],
            contents=[Content.from_dict(y) for y in obj.get("contents") or []],
        )

    @property
    def is_dir(self) -> bool:
        return self.type == "directory"
    
    def walk(self, depth: int = 0):
        yield self, depth
        for child in self.contents:
            yield from child.walk(depth + 1)

@dataclass
class Root:
    type: str
    name: str
    contents: List[Content]

    @classmethod
    def from_dict(cls, obj: list | dict[str, Any]) -> 'Root':
        if isinstance(obj, list):
            obj = next(e for e in obj if e.get("type") != "report")
        
        return cls(
            type=obj["type"],
            name=obj["name"],
            contents=[Content.from_dict(y) for y in obj.get("contents") or []],
        )

    def walk(self):
        for child in self.contents:
            yield from child.walk(depth=1)

