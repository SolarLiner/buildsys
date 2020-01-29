import argparse
import sys
from pathlib import Path
from typing import List

from buildsys.compiler import GccCompiler
from buildsys.ninja import NinjaGenerator
from buildsys.project import ProjectType, Project

CURRENT_DIR = Path(__file__).parent


def main(args: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "build_dir", nargs="?", type=Path, default=CURRENT_DIR / "_build"
    )
    parser.add_argument("source_dir", nargs="?", type=Path, default=CURRENT_DIR)

    args = parser.parse_args(args)
    project = Project("test", ProjectType.Executable)
    project.add_sources(CURRENT_DIR / Path(s) for s in ["src/main.c", "src/lib.c"])
    compiler = GccCompiler(args.source_dir, args.build_dir, project.type)
    generator = NinjaGenerator(compiler)
    generator.generate_project(project)


if __name__ == "__main__":
    main(sys.argv[1:])
