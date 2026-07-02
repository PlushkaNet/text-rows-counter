#!/bin/python3
"""Code rows counter (CRC) source code"""

from typing import Optional
import os
import sys

USAGE_GUIDE_TEMPLATE = \
"""usage: {} [-h --help] [-v --verbose] [-r --recursive] [-d --dir </path/to/directory>] [-f --file <path/to/file>]
Args:
-h, --help - prints this help message
-v, --verbose - prints additional information like currently scanning entry
-r, --recursive - enables recursive scanning for directories
-d, --dir <path/to/directory> - path to directory with text files to scan
-f, --files <path/to/file> - path to file to scan"""

def scan_file(path: str) -> Optional[int]:
    """
    Scans specified file
    Returns number of rows on success
    Returns None on failure
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return len(file.readlines())
    except (OSError, ValueError):
        return None

def scan_dir(path: str, recursive: bool) -> Optional[int]:
    """
    Scans specified directory
    Returns sum of number of rows on success
    Returns None on failure

    This method skips uncountable files (like binaries, which can't be decoded)
    """
    if not os.path.isdir(path):
        return None

    _sum = 0

    for i in os.listdir(path):
        entry_path = os.path.join(path, i)
        if os.path.isdir(entry_path) and recursive:
            _sum += scan_dir(entry_path, True)
        elif count := scan_file(entry_path):
            _sum += count

    return _sum

def main():
    """Main entry for CLI program"""
    NOVALUE = object() # pylint: disable=C0103

    kwargs: dict[str, Optional[list[str]]] = {}
    file_entries = []
    dir_entries = []
    verbose = False
    recursive = False

    argv_last_index = len(sys.argv) - 1
    for i, arg in enumerate(sys.argv):
        if arg.startswith("-"):
            if i < argv_last_index:
                if kwargs.get(arg, None):
                    kwargs[arg].append(sys.argv[i+1])
                else:
                    kwargs[arg] = [sys.argv[i+1]]
            else:
                kwargs[arg] = NOVALUE

    if kwargs.get("--help", None) is not None or kwargs.get("-h", None) is not None:
        print(USAGE_GUIDE_TEMPLATE.format(sys.argv[0]))
        return

    if kwargs.get("--verbose", None) is not None or kwargs.get("-v") is not None:
        verbose = True

    if kwargs.get("--recursive", None) is not None or kwargs.get("-r", None) is not None:
        recursive = True

    if files := kwargs.get("--file", None) or (files := kwargs.get("-f", None)):
        file_entries = files

    if dirs := kwargs.get("--dir", None) or (dirs := kwargs.get("-d", None)):
        dir_entries = dirs

    if not dir_entries and not file_entries:
        dir_entries = ["."]

    def iterate(entries: list, method, verbose: bool):
        sum_lines = 0
        for entry in entries:
            if verbose:
                print(f"scanning: {entry} - ", end="")
            if (result := method(entry)) is not None:
                sum_lines += result
                if verbose:
                    print(f"scanned {result} lines")
            elif verbose:
                print("err")
        return sum_lines

    def _scan_dir_recursive(path: str):
        nonlocal recursive
        return scan_dir(path, recursive)

    _sum_lines = 0
    if verbose:
        print("scanning directories")
    _sum_lines += iterate(dir_entries, _scan_dir_recursive, verbose)
    if verbose:
        print("scanning files")
    _sum_lines += iterate(file_entries, scan_file, verbose)

    print(f"total lines: {_sum_lines}")

if __name__ == "__main__":
    main()
