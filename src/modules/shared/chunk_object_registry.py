from dataclasses import dataclass
from enum import Enum

class ChunkTypeEnum(Enum):
    TOKEN = 'token'
    FILES = 'files'
    METRIC = 'metric'
    DONE = 'done'
    ERROR = 'error'

class TokenChunk:
    def __init__(self, content: str):
        self.type = ChunkTypeEnum.TOKEN
        self.content = content

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "content": self.content
        }

class MetricChunk:
    def __init__(self, name: str, value):
        self.type = ChunkTypeEnum.METRIC
        self.name = name
        self.value = value

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "name": self.name,
            "value": self.value
        }

class DoneChunk:
    def __init__(self):
        self.type = ChunkTypeEnum.DONE

    def to_dict(self) -> dict:
        return {
            "type": self.type.value
        }

class FilesChunk:
    def __init__(self, filenames: list[str]):
        self.type = ChunkTypeEnum.FILES
        self.filenames = filenames

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "filenames": self.filenames
        }

class ErrorChunk:
    def __init__(self, content: str):
        self.type = ChunkTypeEnum.ERROR
        self.content = content

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "content": self.content
        }