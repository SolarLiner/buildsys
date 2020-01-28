from enum import Enum, auto
from pathlib import Path
from typing import List, Iterable

from marshmallow import fields
from marshmallow.schema import Schema


class ProjectType(Enum):
    Executable = auto()
    SharedLibrary = auto()
    StaticLibrary = auto()

    def needs_pic(self):
        return self == ProjectType.SharedLibrary or self == ProjectType.StaticLibrary


class ProjectSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    dependencies = fields.List(fields.Str())
    sources = fields.List(fields.Str())


class Project:
    name: str
    type: ProjectType
    dependencies: List["Project"]
    sources: List[Path]

    def __init__(self, name: str, type: ProjectType = ProjectType.Executable):
        self.name = name
        self.type = type
        self.dependencies = list()
        self.sources = list()

    def add_sources(self, sources: Iterable[Path]):
        for src in sources:
            # if src.exists() and src.is_file():
            self.sources.append(src.resolve())

    def add_dependency(self, project: "Project"):
        self.dependencies.append(project)
