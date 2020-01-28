from pathlib import Path


def relative_recursive(src: Path, base: Path):
    if base.samefile(Path("/")):
        return src.absolute()
    try:
        return src.resolve().relative_to(base.resolve())
    except ValueError:
        return Path("..") / relative_recursive(src, base.resolve().parent)
