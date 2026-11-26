#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off entry writer.

Writes a single original one-line office joke to ``entry.txt`` inside the
output directory named by ``$MAKEFUN_OUTPUT_DIR`` (default ``/output``).

The competition gate only accepts a line that is exactly one line long,
non-blank, and between MIN_CHARS and MAX_CHARS characters inclusive.
This program checks the line against those rules before writing anything,
so a bad line fails loudly instead of producing a rejected entry.
"""

import os
import sys

# The joke itself. Keep this byte-for-byte identical: it is the entry.
ENTRY = "Our boss installed a suggestion box \u2014 it's just a shredder with better branding."

# Competition gate limits, in characters (measured after stripping).
MIN_CHARS = 1
MAX_CHARS = 200

DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def validate_line(line):
    """Return the line stripped, or raise ValueError if it breaks the gate.

    Checks, in order: the line is not blank, it contains no newline, and
    its stripped length sits inside [MIN_CHARS, MAX_CHARS].
    """
    cleaned = line.strip()
    if not cleaned:
        raise ValueError("entry is empty or only white space")
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("entry must be a single line")
    length = len(cleaned)
    if length < MIN_CHARS or length > MAX_CHARS:
        raise ValueError(
            "entry must be between %d and %d characters; got %d"
            % (MIN_CHARS, MAX_CHARS, length)
        )
    return cleaned


def output_path(out_dir):
    """Resolve the full path of the entry file inside out_dir."""
    return os.path.join(out_dir, OUTPUT_FILENAME)


def write_entry(line, out_dir):
    """Validate the line, then write it (plus a trailing newline) to disk.

    Creates out_dir when needed. Returns the path written.
    """
    checked = validate_line(line)
    os.makedirs(out_dir, exist_ok=True)
    path = output_path(out_dir)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(checked)
        handle.write("\n")
    return path


def resolve_output_dir():
    """Pick the output directory from the environment, falling back safely."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return chosen


def main(argv=None):
    """Entry point: validate the joke and write it out. Returns an exit code."""
    del argv  # no command-line arguments are used
    try:
        path = write_entry(ENTRY, resolve_output_dir())
    except (ValueError, OSError) as exc:
        print("cannot write entry: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
