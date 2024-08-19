# Taair
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
# See LICENSE file for details.
import re
from typing import Any
from typing import Type
from typing import TypeVar

from .database import Skill
from .icons import SKILL_SPRITE_MAP

T = TypeVar("T")


def clean_name(name: str) -> str:
    return re.sub("<.*?>", "", name).strip()


SKILL_STYLE_MAP = {"C4": "**"}


def instantiate_dummy(cls: Type[T], **data: Any) -> T:
    default_values: dict[type, Any] = {
        int: 0,
        str: "",
        list: [],
        float: 0.0,
        bool: False,
    }

    return cls(
        **data,
        **{
            key: data.get(key, default_values.get(val_t))
            for key, val_t in cls.__annotations__.items()
            if key not in data
        },
    )


DUMMY_SKILL = instantiate_dummy(Skill, id=0, name="!Not found!", desc="/")


def format_skill_desc(desc: str) -> str:
    style_stack: list[str] = []

    def handle_match(match: re.Match[str]) -> str:
        _, key, value, end = match.groups()
        if end == "/style":
            return style_stack.pop()
        match key:
            case "style":
                style_str = SKILL_STYLE_MAP.get(value, "")
                style_stack.append(style_str)
                return style_str
            case "sprite":
                return SKILL_SPRITE_MAP.get(value, "")
            case _:
                raise NotImplementedError(f"Unimplemented css class: {key}")

    return re.sub(r'<((\w+)="?(\w+)"?)?(.*?)>', handle_match, desc).strip()
