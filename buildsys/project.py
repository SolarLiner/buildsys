from enum import Enum
from pathlib import Path
from typing import List, Iterable

from marshmallow import fields, validates, ValidationError
from marshmallow.schema import Schema


class ProjectType(Enum):
    Executable = "executable"
    Library = "library"

    def needs_pic(self):
        return self == ProjectType.SharedLibrary or self == ProjectType.StaticLibrary


class ProjectSchema(Schema):
    name = fields.Str()
    type = fields.Str(default="executable")
    dependencies = fields.List(fields.Str())
    sources = fields.List(fields.Str())

    @validates("type")
    def validate_type(self, value: str):
        try:
            ProjectType(value)
        except ValueError:
            raise ValidationError("Type must be one of 'executable' or 'library'.")


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

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def add_sources(self, sources: Iterable[Path]):
        for src in sources:
            # if src.exists() and src.is_file():
            self.sources.append(src.resolve())

    def add_dependency(self, project: "Project"):
        self.dependencies.append(project)
