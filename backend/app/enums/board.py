from enum import Enum


class BoardStatus(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"