import shutil
from argparse import ArgumentParser
from pathlib import Path

import yaml

from buildsys.compiler import GccCompiler
from buildsys.ninja import NinjaGenerator
from buildsys.project import ProjectSchema, Project, ProjectType


def resolve_path(path: str):
    return Path(path).resolve()


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "source_dir",
        nargs="?",
        default=Path.cwd(),
        type=resolve_path,
        help="Source directory",
    )
    parser.add_argument("build_dir", type=resolve_path, help="Build directory")
    parser.add_argument(
        "--shared", action="store_true", default=False, help="Build libraries as static"
    )
    parser.add_argument(
        "--static-exe",
        action="store_true",
        default=False,
        help="Build executables statically",
    )

    return parser.parse_args()


def main():
    args = get_args()
    if args.build_dir.is_dir():
        shutil.rmtree(str(args.build_dir))
    project = load_project(args.source_dir)

    compiler = GccCompiler(args.source_dir, args.build_dir, project.type)
    NinjaGenerator(compiler).generate_project(project)


def load_project(source_dir: Path):
    print("Loading", source_dir)
    project_file: Path = source_dir / "project.yml"
    schema = ProjectSchema()
    project_data = schema.load(yaml.safe_load(project_file.open("r")))
    project = Project(project_data["name"], ProjectType(project_data["type"]))
    if "dependencies" in project_data:
        for d in project_data["dependencies"]:
            project.add_dependency(load_project(source_dir / "modules" / d))
    return project


if __name__ == "__main__":
    main()
