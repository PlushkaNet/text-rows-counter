#!/usr/bin/python3
"""
Text rows counter (TRC) - Utility for counting lines in text files and directories.

This module provides functionality to count lines in text files, either individually or 
recursively within directories. It supports both file-based and directory-based counting
with optional verbose output and recursive scanning.
"""

from typing import Optional, List
import argparse
import os


def scan_file(path: str) -> Optional[int]:
    """
    Scan a specified file and count the number of lines in it.
    
    Args:
        path (str): The path to the file to scan
        
    Returns:
        Optional[int]: Number of lines in the file if successful, None on failure
        
    Note:
        This function handles encoding errors gracefully by returning None
        for files that cannot be read or decoded as UTF-8.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return len(file.readlines())
    except (OSError, ValueError, UnicodeDecodeError):
        return None


def scan_dir(path: str, recursive: bool) -> Optional[int]:
    """
    Scan a specified directory and count the total number of lines in all text files.
    
    Args:
        path (str): The path to the directory to scan
        recursive (bool): Whether to scan subdirectories recursively
        
    Returns:
        Optional[int]: Total number of lines in all text files if successful, None on failure
        
    Note:
        This function skips uncountable files (like binaries, which can't be decoded)
        and returns None if the path is not a valid directory.
    """
    if not os.path.isdir(path):
        return None

    _sum = 0

    try:
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path) and recursive:
                result = scan_dir(entry_path, True)
                if result is not None:
                    _sum += result
            elif os.path.isfile(entry_path):
                count = scan_file(entry_path)
                if count is not None:
                    _sum += count
    except (OSError, PermissionError):
        return None

    return _sum


def main() -> None:
    """
    Main entry point for the CLI program.
    
    Parses command line arguments and executes the counting operation.
    Supports scanning of files and directories with optional recursive and verbose modes.
    """
    argparser = argparse.ArgumentParser(
        description="Text rows counter - counts lines in text files and directories",
        allow_abbrev=False
    )
    argparser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="enables display of additional information during scanning"
    )
    argparser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="enables recursive scan of subdirectories"
    )
    argparser.add_argument(
        "-f", "--file",
        action="append",
        help="add target file to scan (can be used multiple times)",
        default=[]
    )
    argparser.add_argument(
        "-d", "--dir",
        action="append",
        help="add target directory to scan (can be used multiple times)",
        default=[]
    )
    
    args = argparser.parse_args()

    # If no directories or files specified, default to current directory
    if not args.dir and not args.file:
        args.dir = ["."]

    def iterate(entries: List[str], method, verbose: bool) -> int:
        """
        Iterate through entries and apply the given method to count lines.
        
        Args:
            entries (List[str]): List of paths to process
            method: Function to call for each path
            verbose (bool): Whether to print verbose output
            
        Returns:
            int: Total lines counted
        """
        sum_lines = 0
        for entry in entries:
            if verbose:
                print(f"scanning: \"{entry}\" - ", end="")
                
            result = method(entry)
            if result is not None:
                sum_lines += result
                if verbose:
                    print(f"scanned {result} lines")
            elif verbose:
                print("err")
                
        return sum_lines

    def _scan_dir_recursive(path: str) -> Optional[int]:
        """Wrapper function for recursive directory scanning."""
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
