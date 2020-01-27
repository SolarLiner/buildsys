from enum import Enum, enum, auto
from pathlib import Path
from marshmallow import fields
from marshmallow.schema import Schema
from typing import List, Iterable


@enum
class ProjectType(Enum):
    Executable = auto()
    Library = auto()


class ProjectSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    dependencies = fields.List(fields.Str())
    sources = fields.List(fields.Str())


class Project:
    name: str
    type: ProjectType
    dependencies: List[Project]
    sources: List[Path]

    def __init__(self, name: str, type: ProjectType = ProjectType.Executable):
        self.name = name
        self.type = type
        self.dependencies = list()
        self.sources = list()

	def add_sources(self, sources: Iterable[Path]):
		for src in sources:
			if src.exists() and src.is_file():
				self.sources.append(src)

	def add_dependency(self, project: Project):
		self.dependencies.append(project)
