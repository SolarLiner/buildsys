import os
from pathlib import Path
from shutil import which

from buildsys.compiler import BaseCompiler
from buildsys.util import relative_recursive
from buildsys.generators import BaseGenerator
from buildsys.generators.ninja.syntax import Writer
from buildsys.project import Project


class NinjaGenerator(BaseGenerator):
    def __init__(self, compiler: BaseCompiler):
        super().__init__(compiler)
        _ccbin = os.getenv("CC", "gcc")
        self.bin = which(_ccbin)
        if self.bin is None:
            raise IOError(f"Binary {_ccbin} could not be found")
        self.bin = Path(self.bin).resolve()

    def generate_project(self, project: Project):
        super().generate_project(project)
        write = Writer((self.build_dir / "ninja.build").open("w+"))
        write.variable("cflags", "-Wall -g")
        write.rule("cc", command=f"{self.bin} -c $in -o $out $cflags")
        write.rule("link", command=f"{self.bin} $in -o $out $ldargs")
        objs = list()
        for src in project.sources:
            obj_path = str(src.relative_to(self.source_dir).with_suffix(".o"))
            src_path = str(relative_recursive(src, self.build_dir))
            write.build(obj_path, "cc", src_path)
            objs.append(obj_path)
        write.build(project.name, "link", objs)
        write.default(project.name)
        write.close()
