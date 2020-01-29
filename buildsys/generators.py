from buildsys.compiler import BaseCompiler
from buildsys.project import Project


class BaseGenerator:
    compiler: BaseCompiler

    def __init__(self, compiler: BaseCompiler):
        self.compiler = compiler

    @property
    def build_dir(self):
        return self.compiler.build_dir

    @property
    def source_dir(self):
        return self.compiler.source_dir

    def generate_project(self, project: Project):
        if not self.build_dir.exists():
            self.build_dir.mkdir(0o755, parents=True)
        elif self.build_dir.exists() and not self.build_dir.is_dir():
            raise IOError("Build directory exists but is not a directory")
        elif (
            self.build_dir.exists()
            and self.build_dir.exists()
            and len(list(self.build_dir.iterdir())) > 0
        ):
            raise IOError("Build directory exists and is not empty")
