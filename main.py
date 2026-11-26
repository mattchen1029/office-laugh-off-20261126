"""Write one original one-line office joke to /output/entry.txt.

The line must stand entirely on its own: one line, 1-200 characters,
not only white space. The gate refuses anything outside that range.
"""

import os
import sys

LINE = "Our boss installed a suggestion box \u2014 it's just a shredder with better branding."

MIN_CHARS = 1
MAX_CHARS = 200


def validate_line(line):
    """Check the line against the competition gate before writing it."""
    stripped = line.strip()
    if not stripped:
        raise ValueError("line is empty or only white space")
    if "\n" in stripped:
        raise ValueError("line must be a single line")
    if not MIN_CHARS <= len(stripped) <= MAX_CHARS:
        raise ValueError(
            "line must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(stripped))
        )
    return stripped


def write_entry(line, out_dir):
    """Write the validated line to entry.txt inside out_dir."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    return path


def main():
    try:
        line = validate_line(LINE)
    except ValueError as exc:
        print("invalid line: %s" % exc, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(line, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
