"""The Printer Finally Answers -- make.fun entry.

Writes the printer's one-line comeback to entry.txt inside the output
directory named by MAKEFUN_OUTPUT_DIR (treated as a directory path).
Pure standard library, fully deterministic.
"""

import os
import sys
import tempfile

ENTRY = (
    "Error 51: I fed 41,208 sheets perfectly, then sheet 41,209 folded "
    "itself \u2014 and you thump me? Six years. Zero thank-yous. "
    "Today I print nothing."
)


def resolve_output_dir():
    """Return a writable directory for entry.txt.

    MAKEFUN_OUTPUT_DIR is a directory path. When it is unset, empty, or
    names something that is not a directory, fall back to /output, then
    the current directory, then the system temp dir.
    """
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir and os.path.isdir(env_dir):
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append(os.getcwd())
    candidates.append(tempfile.gettempdir())
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            probe = os.path.join(path, ".makefun_write_probe")
            with open(probe, "w", encoding="utf-8") as handle:
                handle.write("ok")
            os.unlink(probe)
            return path
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main():
    line = ENTRY
    if not line or not line.strip() or len(line) > 240:
        raise ValueError("entry line must be 1-240 non-blank characters")
    out_dir = resolve_output_dir()
    out_path = os.path.join(out_dir, "entry.txt")
    fd = os.open(out_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    handle = os.fdopen(fd, "w", encoding="utf-8", newline="")
    with handle:
        handle.write(line)
    os.chmod(out_path, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
