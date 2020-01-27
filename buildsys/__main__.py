from pathlib import Path

from buildsys.compiler import GccCompiler
from buildsys.generator import RawCommandsGenerator
from buildsys.project import Project, ProjectType


def main():
    project = Project("test", ProjectType.SharedLibrary)
    project.add_sources([Path("main.c"), Path("lib.c"), Path("hashlib.c")])
    compiler = GccCompiler(Path("."), Path("_build"), project.type)
    generator = RawCommandsGenerator(compiler)
    generator.generate_project(project)


if __name__ == "__main__":
    main()
