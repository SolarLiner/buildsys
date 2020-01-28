import os
import subprocess
from pathlib import Path
from shutil import which
from typing import List, Iterable, TextIO, Union

from buildsys.compiler import BaseCompiler
from buildsys.generators import BaseGenerator
from buildsys.project import Project
from buildsys.util import relative_recursive


class MakefileRule:
    def __init__(self, name: str, *dependencies: str):
        self.code = list()
        self.name = name
        self.dependencies = dependencies

    def add_code(self, code: Iterable[str]):
        self.code.extend(list(code))

    def render(self, f: TextIO):
        f.write(f"{self.name}: {' '.join(str(s) for s in self.dependencies)}\n")
        for code in self.code:
            f.write(f"\t{code}\n")
        f.write("\n")


class MakefileGenerator(BaseGenerator):
    rules: List[MakefileRule]

    def __init__(self, compiler: BaseCompiler):
        super().__init__(compiler)
        self.rules = list()
        self.variables = list()
        _ccbin = os.getenv("CC", "gcc")
        self.bin = which(_ccbin)
        if self.bin is None:
            raise IOError(f"{_ccbin}: No executable found")

    def generate_project(self, project: Project):
        super().generate_project(project)
        for src in project.sources:
            out_dir = self.build_dir / (src.parent.relative_to(self.source_dir))
            if not out_dir.exists():
                out_dir.mkdir(parents=True)
        rule_all = self.create_rule("all", project.name)
        objs = [self.get_dependencies(src) for src in project.sources]
        rule_project = self.create_rule(
            project.name, *[obj.relative_to(self.build_dir) for obj in objs]
        )
        rule_project.add_code([f"{self.bin} $^ -o $@"])
        self.create_rule(".PHONY", rule_all)

        self.render_project()

    def render_project(self):
        makefile = self.build_dir / "Makefile"
        with makefile.open("w") as f:
            for rule in self.rules:
                rule.render(f)

    def create_rule(self, name: str, *dependencies: Union[str, MakefileRule]):
        rule = MakefileGenerator.MakefileRule(
            name, *[d.name if isinstance(d, MakefileRule) else d for d in dependencies],
        )
        self.rules.append(rule)
        return rule

    def add_variable(self, name: str, contents: str):
        self.variables.append((name, contents))

    def get_dependencies(self, src: Path):
        relative = relative_recursive(src, self.build_dir)
        prog = subprocess.run(
            [self.bin, "-MM", relative],
            cwd=self.build_dir,
            stdout=subprocess.PIPE,
            encoding="utf-8",
            check=True,
        )
        name, dependencies = tuple(s.strip() for s in prog.stdout.split(":", 2))
        obj = src.relative_to(self.source_dir).with_name(name)
        rule = self.create_rule(str(obj), dependencies)
        rule.add_code([f"{self.bin} -c $< -o $@"])

        return self.build_dir / obj
