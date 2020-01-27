import abc
from pathlib import Path
from .project import Project


class BaseGenerator:
    build_dir: Path
    def __init__(self, builddir: Path):
        self.build_dir = builddir

    @abc.abstractmethod
    def generate_project(self, project: Project):
        pass


class MakefileGenerator(BaseGenerator):
    def generate_project(self, project: Project):
        makefile_path = self.build_dir / "Makefile"

    def generate_object(self, source: Path):
        object = self.build_dir / source.
