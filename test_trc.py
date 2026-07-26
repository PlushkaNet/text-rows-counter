#!/usr/bin/python3
"""
Test suite for Text Rows Counter (TRC) utility.
Tests all core functionality including file scanning, directory scanning,
error handling, and command-line interface behavior.
"""

import os
import tempfile
import unittest
from unittest.mock import patch
import sys

# Add the current directory to path so we can import trc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import trc


class TestTRC(unittest.TestCase):
    """Test cases for TRC utility functions."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()
        
    def create_test_file(self, filename, content):
        """Helper to create a test file with given content."""
        filepath = os.path.join(self.temp_dir.name, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
        
    def test_scan_file_success(self):
        """Test successful file scanning."""
        # Create test file with known content
        test_content = "Line 1\nLine 2\nLine 3\n"
        filepath = self.create_test_file("test.txt", test_content)

        result = trc.scan_file(filepath)
        self.assertEqual(result, 3)
        
    def test_scan_file_not_exists(self):
        """Test scanning a non-existent file."""
        result = trc.scan_file("/non/existent/file.txt")
        self.assertIsNone(result)
        
    def test_scan_file_invalid_encoding(self):
        """Test scanning a file with invalid encoding."""
        # Create a binary file (this will cause UnicodeDecodeError when read as text)
        filepath = os.path.join(self.temp_dir.name, "binary.bin")
        with open(filepath, 'wb') as f:
            f.write(b'\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\rIHDR')
            
        result = trc.scan_file(filepath)
        self.assertIsNone(result)
        
    def test_scan_dir_success(self):
        """Test successful directory scanning."""
        self.create_test_file("file1.txt", "Line 1\nLine 2\n")
        self.create_test_file("file2.txt", "Line 1\nLine 2\nLine 3\n")

        result = trc.scan_dir(self.temp_dir.name, recursive=False)
        self.assertEqual(result, 5)  # 2 + 3 lines
        
    def test_scan_dir_not_exists(self):
        """Test scanning a non-existent directory."""
        result = trc.scan_dir("/non/existent/dir", recursive=False)
        self.assertIsNone(result)
        
    def test_scan_dir_empty(self):
        """Test scanning an empty directory."""
        result = trc.scan_dir(self.temp_dir.name, recursive=False)
        self.assertEqual(result, 0)
        
    def test_scan_dir_recursive(self):
        """Test recursive directory scanning."""
        # Create nested directories
        subdir = os.path.join(self.temp_dir.name, "subdir")
        os.makedirs(subdir)

        self.create_test_file("file1.txt", "Line 1\nLine 2\n")
        self.create_test_file("subdir/file2.txt", "Line 1\nLine 2\nLine 3\n")
        
        result = trc.scan_dir(self.temp_dir.name, recursive=True)
        self.assertEqual(result, 5)  # 2 + 3 lines
        
    def test_scan_dir_with_binary_file(self):
        """Test scanning directory with binary files (should be skipped)."""
        # Create a text file and a binary file
        self.create_test_file("text.txt", "Line 1\nLine 2\n")
        
        binary_path = os.path.join(self.temp_dir.name, "binary.bin")
        with open(binary_path, 'wb') as f:
            f.write(b'\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\rIHDR')
            
        result = trc.scan_dir(self.temp_dir.name, recursive=False)
        self.assertEqual(result, 2)  # Only text file should be counted
        
    def test_scan_dir_permissions_error(self):
        """Test handling of permission errors during directory scan."""
        with patch('os.listdir') as mock_listdir:
            mock_listdir.side_effect = PermissionError("Permission denied")
            result = trc.scan_dir("/some/path", recursive=False)
            self.assertIsNone(result)
            
    def test_scan_file_permissions_error(self):
        """Test handling of permission errors when scanning file."""
        # Create a file that we can't read
        filepath = self.create_test_file("test.txt", "Line 1\nLine 2\n")
        
        with patch('builtins.open', side_effect=PermissionError("No permission")):
            result = trc.scan_file(filepath)
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
