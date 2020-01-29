import os
from pathlib import Path
from shutil import which

from buildsys.compiler import BaseCompiler
from buildsys.generators import BaseGenerator
from buildsys.ninja.syntax import Writer
from buildsys.project import Project
from buildsys.util import relative_recursive, iter_includes


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
        write = Writer((self.build_dir / "build.ninja").open("w+"))
        deps = list()
        for dep in project.dependencies:
            builddir = self.build_dir / dep.name.replace(" ", "_")
            compiler = self.compiler.__class__(
                self.source_dir / "modules" / dep.name, builddir, dep.type
            )
            generator = NinjaGenerator(compiler)
            generator.generate_project(dep)
            write.subninja(
                str(relative_recursive(builddir / "build.ninja", self.build_dir))
            )
            deps.append(builddir / dep.name)

        write.variable(
            "cflags",
            " ".join(
                [
                    "-Wall",
                    "-g",
                    "-I" + str(relative_recursive(self.source_dir, self.build_dir)),
                    *[
                        "-I"
                        + str(
                            relative_recursive(
                                self.source_dir / "modules" / d.name, self.build_dir
                            )
                        )
                        for d in project.dependencies
                    ],
                    *[
                        "-I" + str(relative_recursive(s, self.build_dir))
                        for s in iter_includes(project, self.source_dir)
                    ],
                ]
            ),
        )
        write.rule("cc", command=f"{self.bin} -c $in -o $out $cflags")
        write.rule("link", command=f"{self.bin} $in -o $out $ldargs")
        objs = list()
        for src in project.sources:
            obj_path = str(src.relative_to(self.source_dir).with_suffix(".o"))
            src_path = str(relative_recursive(src, self.build_dir))
            write.build(obj_path, "cc", src_path)
            objs.append(obj_path)

        write.build(
            project.name, "link", list(map(str, map(relative_recursive, deps + objs)))
        )
        write.default(project.name)
        write.close()
