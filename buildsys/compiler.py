import abc
from pathlib import Path
from typing import List

from buildsys.project import ProjectType
from buildsys.util import relative_recursive


class BaseCompiler(abc.ABC):
    def __init__(self, source_dir: Path, build_dir: Path, buildtype: ProjectType):
        self.source_dir = source_dir.resolve()
        self.build_dir = build_dir.resolve()
        self.build_type = buildtype

    @abc.abstractmethod
    def compile(self, input: Path, output: Path, includes: List[Path]):
        pass

    @abc.abstractmethod
    def link(self, inputs: List[Path], output: Path, args: List[str]):
        pass


class GccCompiler(BaseCompiler):
    def compile(self, input: Path, output: Path, includes: List[Path]):
        args = ["gcc"]
        if self.build_type.needs_pic():
            args.append("-fPIC")
        args.extend(["-c", (relative_recursive(input, self.build_dir))])
        args.extend(["-I.", f"-I{relative_recursive(self.source_dir, self.build_dir)}"])
        args.extend(
            f"-I{relative_recursive(include, self.build_dir)}" for include in includes
        )
        args.extend(["-o", (relative_recursive(output, self.build_dir))])
        return args

    def link(self, objects: List[Path], output: Path, link_args: List[str]):
        args = ["gcc"]
        if self.build_type == ProjectType.SharedLibrary:
            args.append("-shared")
        elif self.build_type == ProjectType.StaticLibrary:
            args.append("-static")
        args.append("-L.")
        for arg in link_args:
            args.append(f"-l{arg}")
        for obj in objects:
            args.append(relative_recursive(obj, self.build_dir))
        args.append("-o")
        args.append(relative_recursive(output, self.build_dir))
        return args
