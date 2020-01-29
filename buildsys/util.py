from pathlib import Path

import buildsys.project


def relative_recursive(src: Path, base: Path):
    if base.samefile(Path("/")):
        return src.absolute()
    try:
        return src.resolve().relative_to(base.resolve())
    except ValueError:
        return Path("..") / relative_recursive(src, base.resolve().parent)


def iter_includes(project: "buildsys.project.Project", source_dir: Path):
    include_dir = source_dir / "include"
    if include_dir.exists() and include_dir.is_dir():
        yield include_dir
    for d in project.dependencies:
        include_dir = source_dir / "modules" / d.name / "include"
        if include_dir.exists() and include_dir.is_dir():
            yield include_dir
        for include_dir in iter_includes(d, include_dir.parent):
            yield include_dir
