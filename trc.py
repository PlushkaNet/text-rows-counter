#!/usr/bin/python3
"""Text rows counter (TRC) source code"""

from typing import Optional
import argparse
import os

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

    argparser = argparse.ArgumentParser(description="text rows counter", allow_abbrev=False)
    argparser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="enables display of additional information"
    )
    argparser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="enables recursive scan"
    )
    argparser.add_argument(
        "-f", "--file",
        action="append",
        help="add target file to scan",
        default=[]
    )
    argparser.add_argument(
        "-d", "--dir",
        action="append",
        help="add target directory to scan",
        default=[]
    )
    args = argparser.parse_args()

    if not args.dir and not args.file:
        args.dir = ["."]

    def iterate(entries: list, method, verbose: bool):
        sum_lines = 0
        for entry in entries:
            if verbose:
                print(f"scanning: \"{entry}\" - ", end="")
            if (result := method(entry)) is not None:
                sum_lines += result
                if verbose:
                    print(f"scanned {result} lines")
            elif verbose:
                print("err")
        return sum_lines

    def _scan_dir_recursive(path: str):
        return scan_dir(path, args.recursive)

    _sum_lines = 0
    if args.verbose:
        print("scanning directories")
    _sum_lines += iterate(args.dir, _scan_dir_recursive, args.verbose)
    if args.verbose:
        print("scanning files")
    _sum_lines += iterate(args.file, scan_file, args.verbose)

    print(f"total lines: {_sum_lines}")

if __name__ == "__main__":
    main()
